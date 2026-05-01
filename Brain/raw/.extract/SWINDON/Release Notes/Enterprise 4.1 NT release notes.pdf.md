BroadVision One-To-One

Version 4.1 for Windows NT

Server Release Notes

This is Version 4.1 of BroadVision® One-To-One™ Enterprise for the Windows NT platform. This
document includes information about these topics:

l “Included in this release” on page 2.

l “License agreement” on page 2

l “Technical support” on page 3.

l “Documentation” on page 4.

l “System and software requirements” on page 5.

l “What’s new or changed in Version 4.1” on page 7.

• “New bv1to1.conf parameters” on page 9.

• “Database changes” on page 13.

• “API changes” on page 14

l “Installing One-To-One Version 4.1” on page 15.

• “Migration notes” on page 16.

l “Problems ﬁxed in the Version 4.1 release” on page 18.

l “Known One-To-One problems, and issues” on page 18.

l “Tips for using One-To-One Enterprise” on page 22.

l “Supplemental documentation” on page 25.

• “Accessing properties with BVI_Properties” on page 25

• “Cheap sessions and BV_SmgrSessionHandle” on page 26

• “Clariﬁcation of system() command examples” on page 27

• “Loading observations to Oracle across platforms” on page 27

• “Running HTTP on a machine different from the Interaction Manager host” on page 28

This 4.1 release has been tested and certified to run on Windows NT, version 4.

One-To-One Server Release and Installation Notes

290-41A-NAS

BroadVision, Inc.

2

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Included in this release

Included in this release

In addition to the One-To-One system, this release includes:

l IDL interface ﬁles, C++ header ﬁles, and libraries needed to write One-To-One applications.

l Rogue Wave Tools.h++ version 7.0.2 run-time support.

l Orbix 2.2 with patch 2.2c17 for Windows NT 4.0.

• If you are going to develop custom servers that require the Orbix IDL compiler, you need to
acquire a full-use Orbix license from BroadVision or IONA Technologies, Ltd. If you do not
need to compile IDL you do not need a separate license.

• Orbix 2.2 on Windows NT does not have IIOP, and as such, neither does One-To-One.
Additionally, the BVI_NamingContext component is not usable with servers that
communicate via IIOP.

l MKS Toolkit Version 5.2, Intel version.

l The Interaction Manager contains a JavaScript engine compatible with Netscape version 1.2.

l The CD-ROM that contains the application also contains the One-To-One Command Center and
One-To-One Design Center and Report Manager ﬁles. Some of these ﬁles contain both U.S. and
non-U.S. localized versions of these applications.

l Support for Verity Search’97, version 2.4.0. Note that a separate license is required to use the

Verity software included with this release.

License agreement

Use of the accompanying product is governed by the terms of your BroadVision license agreement,
which includes limits on the number of copies that may be installed and used. To simplify the
installation and use of this product, One-To-One is packaged with all available components on each
CD. This packaging does not imply permission to use more copies of the components than is
permitted by your license agreement.

BroadVision, Inc.

290-41A-NAS

One-To-One Server Release and Installation Notes

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Technical support

3

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

BroadVision will support customers who use newer versions of third-party products by working
with the customer to resolve compatibility problems with the third-party vendor. BroadVision will
also consider, at our option, developing and releasing minor ﬁxes for our products in order to
resolve problems with new versions of third-party products.

One-To-One Server Release and Installation Notes

290-41A-NAS

BroadVision, Inc.

4

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Documentation

Documentation

Documentation for BroadVision® One-To-One™ Enterprise is available electronically in HTML and
PDF formats. Additionally, two of the manuals are also reproduced in print. These release notes, and
the One-To-One Command Center Release Notes, are available in print only.

From time to time BroadVision updates the electronic documentation and makes it available to
customers. If you are interested in receiving a notification when updates are available, please
send an e-mail message to bvpubs@broadvision.com, and put “subscribe v41docs” in
the subject field. Notifications will be sent to the reply-address of the message.

To use the HTML or PDF documentation, you can either access it directly from one of the
CD-ROMs, or from the One-To-One system directory. In your browser, enter the URL that points to
the welcome.htm ﬁle.

l If you are using the Application CD-ROM as the target, enter:

file:///E|/PUBS/ONETOONE/Welcome.htm

l If you are using the Documentation CD-ROM as the target, enter:

file:///E|/Welcome.htm

l If you are using the installed files, enter the full path to the ﬁle, such as:

file:///E|/BV1TO1/PUBS/ONETOONE/Welcome.htm

Optionally, you can copy or link the tree into the document root of your HTML server.

Included on the application CD-ROM and in the installed files is a document not listed on the
Welcome.htm page. The Using Dynamic Categories document explains how to implement and
use the One-To-One dynamic categories. This document is available in HTML and PDF formats
in the following locations:

…/PUBS/ONETOONE/EXTRA/dyncat.htm
…/PUBS/ONETOONE/EXTRA/dyncat.pdf

To access the PDF (Portable Document Format) ﬁles, you will need a PDF viewer, such as Adobe’s
Acrobat Reader, which is available for free downloading from Adobe’s Web site at:

http://www.adobe.com/prodindex/acrobat/readstep.html

Additional BroadVision documents and white papers are available at:

http://www.broadvision.com

BroadVision, Inc.

290-41A-NAS

One-To-One Server Release and Installation Notes

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
System and software requirements

5

System and software requirements

The version numbers listed in this document are the ones that BroadVision tested. Later
versions should be acceptable if the manufacturer claims that the later version is compatible.

The One-To-One servers and development environment require:

CPUs and memory — An Intel Pentium II 200 Mhz or better running Windows NT version 4.0 (with
Service Pack 4), and 128 MB of main memory per CPU. If you want to run multiple One-To-One
installations on a single machine, or run other applications on the same machine, you need more
memory.

Disk space — 145 MB of hard disk space to contain the One-To-One system and MKS Toolkit system
(Version 5.2, Intel version is included on the One-To-One CD). Additionally:

• If you plan to install the Verity search software (separate license required), you will need an

additional 102 MB of hard disk space.

• One-To-One requires at least 512 MB of swap space (1 GB preferred). If you want to run
multiple One-To-One installations on a single machine, or run other applications on the
same machine, you need more space. It is important that the machine not run out of swap
space in a deployed application.

• One-To-One stores its information in databases. Allocate at least 35 MB for the body of the
database, and 5 MB for database transaction logging. A production environment will
probably need considerably more. It is important that the database not run out of space in a
deployed application.

• For observation and microtransaction logging on a development system, allocate about

10 MB of disk space. For a production or load-testing environment, estimate 300 to 400 bytes
per estimated hit; for example, with 1 million hits a day, estimate 400 MB per day.

Development systems — require Purify (at least version 6.0) from Rational Software. You must run
Purify on all C++ code written for use in the One-To-One system. Running Purecov is also
recommended because it generates a report detailing how much of your code was touched by your
test cases. Purify requires at least 1 GB of swap space.

One of the following types of networks must be installed:

l A LAN should be 100 Mbps Ethernet or above. Or, at least, an Ethernet switch with a 10 Mbps

channel into each machine.

l A WAN, including modems, with sufﬁcient bandwidth to handle communications between the

site and the visitors. Often, the bottleneck of a Web site is the external network.

l For conﬁgurations with multiple host machines, see the Installation and System Administration

Guide for details. In general,

• Each One-To-One host should be able to mount the location of the $BV1TO1_VAR directory.
Additionally, each Interaction Manager host must either be able to see the $BV1TO1_VAR
directory, or have an copy of the $BV1TO1_VAR directory tree and ﬁles available to it locally.
The Interaction Manager host should be able to see a $BV1TO1 directory

l The machine that will host One-To-One must be registered with your network’s Domain Name
Server (DNS). Even if the machine is running stand-alone — isolated from a network — it must
have a DNS entry.

Networks

One-To-One Server Release and Installation Notes

290-41A-NAS

BroadVision, Inc.

6

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
System and software requirements

Third party options

One-To-One also supports the following third-party software options:

l Verity Search’97, version 2.4.0. Note that a separate license is required to use the Verity software

included with this release.

l Microsoft Visual C++ Version 6.0 with Visual Studio Service Pack 2. The One-To-One makeﬁles

require nmake from this version.

l The AVP Taxware tax package, version 3.0. For more information about using the AVP taxware

package, see the Installation and System Administration Guide.

l An HTTP server:

• Microsoft Internet Information Server (IIS) 4.0 U.S. English, 4.0 German or Japanese, or later.

• Any HTTP server that runs in standard CGI mode should work; however, performance will

not be as good as when using Microsoft Internet Information Server with ISAPI.

l The Rogue Wave development libraries. One-To-One supports these versions:

• Tools.h++ version 7.0.2 to develop client side libraries.

• DBtools.h++ version 2.1.1 if you are doing server development. Otherwise, you don’t need

this package.

• DBTools.h++ 2.1.1 MS SQL or Oracle Access Library.

• Money.h++ version 1.4.1 if you are implementing servers, Dynamic Objects, or components

that use currency. Otherwise, you don’t need this package.

l Orbix 2.2 with patch 2.2c17 for Windows NT 4.0.

You must use the Orbix and Rogue Wave ﬁles supplied in this release when you run
One-To-One. Other versions of Orbix and Rogue Wave are not supported.

l To run reports, the client system needs one of these ODBC drivers:

Oracle 8, version 8.0.5

If your site does e-mail targeting, you will want to use the One-To-One bounced_email_utl
utility to periodically identify those visitors whose e-mail addresses are invalid. See the description
of the utility in the Installation and System Administration Guide. That utility reads a ﬁle of invalid
addresses. To generate the ﬁle from the “bounced” e-mail that your site receives, consider acquiring
one of these third party utilities (addresses are current at the time of this printing):

l SmartBounce from Orion Software, http://www.bsabio.com/SmartBounce/

l Procmail written by S.R. van den Berg. You can download the procmail.tar.gz ﬁle from

various comp.sources.misc archives, such as these:

ftp://ftp.net.ohio-state.edu/pub/networking/mail/procmail/
ftp://hub.ucsb.edu/pub/mail/
ftp://ftp.informatik.rwth-aachen.de/pub/packages/procmail/

Database management system

One of the following database management systems needs to be installed:

Oracle

Oracle Client Version 8.0.5 for Windows NT talking to an Oracle Server: any of the server versions that
the client can talk to — per Oracle — should work.

SQL Server

Microsoft SQL Server (MSSQL) Version 7.0

BroadVision, Inc.

290-41A-NAS

One-To-One Server Release and Installation Notes

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
What’s new or changed in Version 4.1

7

What’s new or changed in Version 4.1

Here are some of the new or improved features of the BroadVision® One-To-One™ Enterprise:

Here are some of the new features of the BroadVision® One-To-One™ Enterprise:

Scripting and components is a new model for generating Web pages. You can still use page templates
and dynamic objects, and there is limited support for mixed-mode operation between these two
models.

Year 2000 support across all One-To-One systems.

Verity full-text search support for licensed customers.

Matching based on content and session proﬁle attributes.

Related content and profile attributes for lists of items that apply to a single attribute.

Site-defined content types.

Visitor notiﬁcations, including e-mail alerts and visitor inboxes.

Access control of executables including scripts, templates, and receive dynamic objects.

Site IDs for content to allow distributed sites to copy content between One-To-One installations.

System monitoring tools.

The Broadway sample application demonstrates a One-To-One application.

Interaction Manager and HTTP server can run on separate machines.

Internationalization and localization support for these languages:

l English and Japanese — Full character set and language support, including a translated

One-To-One Command Center. The Broadway sample application and data remain in English.

l Western European (Latin 1) — These character sets are fully tested and supported, but no

language translations are provided.

l Hebrew, Arabic, Traditional Chinese, Korean, and Turkish — BroadVision has reviewed these

character sets and believes they will work, including support for local currency symbols, and
date/time and number formatting. Note that BroadVision does not test these character sets, and
while Technical Support will respond to problem reports, patches will not be created for them;
though consideration will be given to providing bug ﬁxes in a future product release.

For character sets to work correctly, the database and server character sets must be set to work
with the Windows machines running the One-To-One Command Center. See the Installation and
System Administration Guide for details.

Euro currency is supported so that EMU-located sites may use the euro as either the base or alternate
currency while still supporting the local currency. On platforms with character sets that support the
euro, the euro symbol is available. Additionally,

l The BVI_Money component provides currency conversion that follows the EMU conversion

rules from EMU currencies, both to and from the euro to EMU currencies. The component also
converts currency from any EMU currency to any other EMU currency by converting through
the Euro as provided by EMU conversion rules.

One-To-One Server Release and Installation Notes

290-41A-NAS

BroadVision, Inc.

8

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
What’s new or changed in Version 4.1

Cookie-based session identification to support sending a client-stored cookie with embedded session
information back to the server along with the speciﬁed request.

Database enhancements include:

l Sharing a single database between multiple One-To-One systems. This is especially useful for

large or disparate site installations.

l Automatic re-connection of the One-To-One servers to the database when the connection has

been lost due to the database being shut down and restarted.

l Privacy flags in the visitor proﬁle database are now optional.

l External database support has been added for proﬁle and content data.

Improved debugging support is available through JavaScript method tracing. Scripts may be
monitored to observe when they ran.

Observation logging has been simpliﬁed and performance has been improved and additional data
can now be captured to support more detailed analytic reporting. Also, a JavaScript function now
records when a guest visitor converts to a registered visitor.

Verity full-text search support for licensed customers. Includes support for multiple Western
European languages, along with locale/character map pairing for up to 32 pairs. Note that there is
no Japanese version of Verity version 2.4.0 — the supported version.

Performance has been enhanced through general tuning and incremental performance
improvements, including better load balancing for large conﬁgurations. Additionally,

• New page caching allows speciﬁc pages to be identiﬁed and cached after they are generated

the ﬁrst time, and regenerated a periodic intervals.

The Interaction Manager session handle interface is new and provides a way to call page scripts from
a program running outside of the Interaction Manager, bypassing the HTTP server. This lets non-
BroadVision applications take advantage of BroadVision® One-To-One™ Enterprise functionality
that is provided in a page script. See the Developer’s Guide to Components and Scripts for details.

Changes to previous functionality

Additionally, these areas have changed since the previous release:

l The Interaction Manager now writes core ﬁles, and the CGI gateway writes log ﬁles

subdirectories in the $BV1TO1_VAR directory tree. Previously, it wrote the ﬁles to a /TEMP
directory on the current host.

l New .bvlog.conf settings for new systems.

l Log ﬁlenames now, by default, contain the century in the year portion of the date in the name,

such as bvobs.out.19980812.

l The session ID format that appears in URLs has changed to allow for customization and

separation of HTTP and Interaction Manager servers machines.

l Observation event deﬁnitions are now in $BV1TO1_VAR/etc/bvobs.conf.

For information about changes to the One-To-One Command Center, see the One-To-One Command
Center Release Notes.

BroadVision, Inc.

290-41A-NAS

One-To-One Server Release and Installation Notes

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
What’s new or changed in Version 4.1

9

New bv1to1.conf parameters

To better support One-To-One, and to support new features, the bv1to1.conf conﬁguration ﬁle
contains these new settings. To see examples of the use of these settings, look at the
$BV1TO1/lib/bv1to1.conf.default ﬁle.

This file was reorganized and extensive comments were added to it. As such, a simple “diff” of
the file against your existing configuration is not productive. See the migration instructions in
the Installation and System Administration Guide for details about updating this file if you are
migrating from an older version.

New setting

Description

BV1TO1_INSTANCE

Instance name of the One-To-One conﬁguration.

bv_site_id="0"

bv_y2k_cutoff="30"

BVLOG_DIR

CommandCenter (group)

external_content_write="0"

external_proﬁle_write="0"

privacy_ﬂag="0"

Identiﬁes content items as being created at a speciﬁc
One-To-One site as identiﬁed by the integer. Use this setting to
create OID values that are unique between One-To-One sites,
such as when you have data being created and copied to
distant, related One-To-One sites. This setting does not affect
user IDs, user payment type IDs, account IDs, service (store)
IDs, or order management transactions. The valid range is 0 –
3.

A two-digit year. Dates equal to or greater than this year are
considered to be in the 1900s. Years less than the speciﬁed
year are considered to be in the 2000s. For this 4.1 release,
see the One-To-One Overview manual for details and issues
about using this setting.

Root directory to contain log ﬁles. If not deﬁned, the system
defaults to $BV1TO1_VAR.

New, reserved name, identiﬁes processes to be used by the
Command Center only.

Identiﬁes whether or not content information stored in an
external database is writable. A zero (0) indicates read-only.

Identiﬁes whether or not visitor proﬁle information stored in an
external database is writable. A zero (0) indicates read-only.

Determines whether or not to generate privacy columns for the
visitor proﬁle database tables. When set to one (1), the schema
generator creates a privacy ﬁeld for each deﬁned attribute in
the proﬁle schema. The privacy ﬁeld name begins with “P_”
and is used by your site to indicate the visitor’s preference for
the corresponding proﬁle attribute.

Previous to Version 4.0, this was not an option and the ﬁelds
were always created.

smgr_ﬁrst_port_minimum

New, used by imgr_conf when scanning for available ports.

Payment handler
changes

In Version 3.0, the payment handlers (pmtassign_d, pmtsettle_d, and pmthdlr_d) were
“processes”. Beginning with Version 4.1, they have been changed to “daemons”.

daemon pmthdlr_d ...

One-To-One Server Release and Installation Notes

290-41A-NAS

BroadVision, Inc.

10

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
What’s new or changed in Version 4.1

Notiﬁcation
settings

Notiﬁcation settings.

Notiﬁcation setting

Description

bv_check_want_message_attr

Tells whether or not to verify that a visitor wants messages before
sending a message to the visitor.

bv_email_delivery_server_count The count of e-mail delivery servers speciﬁed in the conﬁguration ﬁle.

By default, there is only one.

bv_email_delivery_addr_attr

Attribute that contains the visitor’s e-mail address.

bv_email_host

The host name of the e-mail server.

bv_schedule_keep_messages

Keeps or removes messages after sending them.

bv_schedule_parallel_count

How many parallel processes to assign to each batch processor.

bv_schedule_dynamic_msgcount Dynamic messages per directory

bv_schedule_static_msgcount

Static messages per directory.

bv_schedule_msg_dir

The parent directory that contains all schedule messages. By default,
this is $BV1TO1_VAR/messages/.

bv_schedule_script_root

Notiﬁcation message generation scripts directory.

bv_schedule_startup_root

Directory of scripts to run when the message generator launches.

Notiﬁcations
handler changes

The Notiﬁcations delivery server has two additional parameters that control how many messages to
send at a time, and how long to wait before sending the next set. The msg_count parameter deﬁnes
the count, and the msg_delay parameter speciﬁes how long to wait.

daemon deliv_smtp_d {

parameter
shutdown="bvkill -w 2 USR1"
id="1"
delay="600"
sleep="120"
msg_count="10"
msg_delay="4"
offline="1"

# Seconds to wait after being launched.
# Seconds to wait between polls.
# Messages to send without waiting.
# Seconds to wait between msg_count sets.

}

In the example above, the offline parameter is set to 1 to enable the e-mail delivery mechanism.
This is off by default. Also, be sure to specify the host machine that will run the smtp service, do that
with the bv_email_host parameter.

bv_email_host="localhost"

Removed since
version 3.0

The adm_srv server is obsolete and no longer included in the release. You should remove
references to it in the bv1to1.conf conﬁguration ﬁle.

BroadVision, Inc.

290-41A-NAS

One-To-One Server Release and Installation Notes

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
What’s new or changed in Version 4.1

11

Global name path settings

The global name path settings identify where One-To-One ﬁnds subsystems in the One-To-One
namespace. Do not change these settings.

New global name paths

alert_path

Description

Alert server

cachecontrol_path

Scheduler cache

extdbacc_path

genericdb_path

schedweb_path

schedbatch_path

External database accessor

Generic database accessor

Schedule web

Schedule batch

schedparallel_path

Schedule parallel

Orbix settings

These settings help control how the CORBA servers and clients behave.

New global name paths

Description

BV_ORB_CONNECT_TIMEOUT Connection time-out (in seconds)

BV_ORB_CALL_TIMEOUT

Call time-out (in seconds)

BV_ORB_DIAGNOSTICS

Diagnostic level

BV_ORB_BIDIRECTIONAL_IIOP Future for Orbix 2.3, not used in 4.1.

IT_MAX_MESSAGE_SIZE

Future for Orbix 2.3, not used in 4.1.

Directory
speciﬁcations

New directory speciﬁcations tell the One-To-One Command Center where to locate ﬁles, scripts,
and page templates. Another parameter identiﬁes where the component libraries are located.

Directory speciﬁcations

Directory

bv_dcc_document_root

The HTTP server’s document root location.

bv_dcc_schedule_root

Notiﬁcation message script root location.

bv_dcc_script_root

The script root location.

bv_dcc_template_root

Page template root location.

bv_js_library_dir

Contains the JavaScript component libraries that the
Interaction Manager accesses. By default, it is
$BV1TO1/lib/components, and may contain component libraries
only; no other ﬁle types are allowed in this directory.

One-To-One Server Release and Installation Notes

290-41A-NAS

BroadVision, Inc.

12

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
What’s new or changed in Version 4.1

Cache settings

The database accessors and Interaction Manager servers cache database data to improve
performance. These settings specify the memory size of speciﬁc caches, and the limits to the count of
items that a cache may store.

Cache setting

cat_cache_size

cnt_type_cache_size

Description

Categories cache size.

Cache sizes for speciﬁc content types. A speciﬁcation in this setting
overrides the default cache size speciﬁed by
default_cnt_cache_size. To specify sizes, include the content
name and size, the name must be same as the content type name in
the content map table. For example:

"PRODUCT=300, AD=200, MSGSCRIPT=0"

Set a cache size to 0 when you do not want to cache data, such as
when retrieving timely, dynamic data from an external data source.

default_cnt_cache_size

The default cache size to use for all content types.

gdb_query_cache_size

New, generic database accessor query cache size.

gdb_query_cache_timeout

New, generic database accessor query cache time-out limit.

gdb_query_limit

query_cache_size

New, generic database accessor return count limit.

The count (in thousands), of IDs to store as result of a query. Each ID
requires 4 bytes of memory.

query_cache_timeout

New, query cache time-out limit.

query_limit

The maximum count of IDs to cache per query. If a query exceeds the
limit, it is not cached.

rule_cache_size

Matching rules cache size.

Process
declarations

New processes identify new servers.

Process declaration

adm_srv (process)

alert_srv

extdbacc

genericdb

sched_srv

Description

Obsolete, not used, and removed in 4.1.

The alert server.

The external database accessor. You must use this if you are
accessing an external database.

The generic database accessor.

The scheduling server.

Daemon
deﬁnitions

New server daemons control e-mail targeting and scheduling processes.

Daemon processes

Description

sched_poll_d

deliv_smtp_d

deliv_comp_d

Scheduler daemon; only one per site.

E-mail delivery daemon; there can be many deliv_smtp_d daemons
with unique ID values identifying each. Each process communicates
with the e-mail server deﬁned by the bv_email_host setting.

Delivery completion daemon; only one per site, and there must be one
if you have a deliv_smtp_d daemon.

BroadVision, Inc.

290-41A-NAS

One-To-One Server Release and Installation Notes

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
What’s new or changed in Version 4.1

13

Database changes

These database schema items have changed since the previous release.

l Content tables all have three new attributes: RATING, NO_VOTES, and TOTAL_RATING

Table

BV_ADMIN_USER

BV_ALERTSCHED

BV_ALERTSTAT

BV_ATTR_GROUP

BV_ATTR_GROUP_INFO

BV_ATTRIBUTES_EXT

BV_BUY

BV_BUY_MT

Change

New

New

New

New

New

New

Has new attribute: USER_ID

Has new attribute: USER_ID

BV_CATEGORY_PATH

New table to contain category pathnames for use by reports.

BV_CHOOSE

BV_COLLECTION

Has new attribute: USER_ID

Has new and removed attributes to reﬂect change to content-type and
collection ﬂags.

BV_COMMUNITY

Has new and removed attributes to reﬂect change to content-type

BV_END_SESSION

Has new attribute: USER_ID

BV_ENTER_STORE

Has new attribute: USER_ID

BV_EXT_MAP table

BV_MSGSCHED

BV_MSGSCRIPT

BV_MSGSTAT

New

New

New

New

BV_OBS_USER_DEFINED

Has new attribute: USER_ID

BV_PROD_TRANSLATE

New

BV_PROFILE_2

BV_PROFILE_3

BV_QUERY

BV_REMOVE

BV_RULE_TARGET

Removed

Removed

New

Has new attribute: USER_ID

Has new attributes: TARGET_ORDER_BY, TARGET_ORDER_TYPE,
TARGET_FLAGS, TARGET_CNT_QUERY, TARGET_QUERY_OID, &
TARGET_SESN_RULE.

BV_SCHEMA_VERSIONS

New

BV_SCRIPTS

BV_SEE

BV_SEE_AD

BV_SELECT

New table to contain references to page scripts. The content type ID is
14.

Has new attribute: USER_ID

Has new attribute: USER_ID

Has new attribute: USER_ID

BV_SELECT_AD

Has new attribute: USER_ID

BV_TARGET_FUNC

Has new and removed attributes

BV_TARGETING_RULE

Has new attribute: USER_ID

BV_TAXON_MAP

New

One-To-One Server Release and Installation Notes

290-41A-NAS

BroadVision, Inc.

14

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
What’s new or changed in Version 4.1

Table

BV_TYPE_USAGE

Change

New

BV_USER_PROFILE

New attributes

BV_USER_PROFILE.
LAST_MOD_TIME

New attribute to identify when the visitor’s proﬁle was last updated.

BV_USER_ROLE

New

API changes

These API have changed since the previous release.

BV_ContentDB::
modify_content_with_time()

New member.

BV_DMem::Operation

Added two operations: MIN and MAX

BV_MultiValueUpdates::
BV_ModifyOperation

BV_NSLookupCache::
set_preferred_group()

New member.

New member.

BV_RuleDB

Added user_id argument to these members:

• insert_collection()
• delete_collection()
• update_collection()
• insert_rule()
• delete_rule()
• update_rule()
• insert_community()
• delete_community()
• update_community()

BV_SmgrSessionHandle

New interface to call the Interaction Manager without going through an
HTTP server. See the Developer’s Guide to Components and Scripts for
details.

BV_Proﬁle

Removed update(), it was never implemented.

BV_ProﬁleManager

Removed update_ranges(), it was never implemented.

BroadVision, Inc.

290-41A-NAS

One-To-One Server Release and Installation Notes

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Installing One-To-One Version 4.1

15

Installing One-To-One Version 4.1

If you intend to install the One-To-One Enterprise Broadway sample application, you must
install it before installing any BroadVision One-To-One applications, such as One-To-One
Publishing Center, One-To-One Commerce, One-To-One Financial, or One-To-One Knowledge.

CAUTION Never:

• Install one version of One-To-One on top of an existing version. Always uninstall the old

version ﬁrst, or install the new version in a new location.

• Hard code database passwords in the bv1to1.conf conﬁguration ﬁle. Passwords should

be entered in response to a prompt in the conﬁguration ﬁle.

Notiﬁcation system

When setting up a notiﬁcation system, it is important to put sched_header.jsp in the
bv_schedule_script_root directory (which is deﬁned in the bv1to1.conf ﬁle). There is a
default copy in $BV1TO1/lib/. Customize the sched_header.jsp ﬁle if you implement a
custom delivery method.

Oracle installations

When installing the Oracle 8 client, select the “administrator” option. This copies utilities that are
not available to a client, but which are necessary to One-To-One, such sqlldr80.exe.

Start-up fails with error 1068

If One-To-One fails to start and returns an error code of 1068, check the Windows NT event log. If
the unavailable service is “net logon” and you are using a stand-alone (single-host) machine, you
may have entered incorrect domain information when bvconf execute prompted you for user
account: enter the name in the form DOMAIN\USERNAME; on a stand-alone machine, use
MACHINE\USERNAME. Try uninstalling the service and then re-running bvconf execute to enter
the correct domain name. To uninstall the service, use the bvntsvc utility, like this:

$ bvntsvc uninstall
$ bvconf execute

Short-cuts are wrong

The installation program creates shortcuts for starting and stopping the default server instance and
default Interaction Manager application. Each of the shortcuts is missing a semi-colon (;) in its short-
cut command. See “Installation issues” on page 19 for details.

Registry notes

The One-To-One servers and daemons inherit environment variables from the Windows NT registry
entries located in:

\HKEY_LOCAL_MACHINE\SOFTWARE\BroadVision\

One-To-One Application System\4.1\instance\export

One-To-One Server Release and Installation Notes

290-41A-NAS

BroadVision, Inc.

16

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Installing One-To-One Version 4.1

The Interaction Manager servers have conﬁguration information stored in:

\HKEY_LOCAL_MACHINE\SOFTWARE\BroadVision\
One-To-One Application System\4.1\
Interaction Manager\application\export

Multiple-host environments

When running in a multiple-host environment, as described in the Installation and System
Administration Guide, all servers on all host machines must be started using the same user account.

See “Running HTTP on a machine different from the Interaction Manager host” on page 28 of
this document if you are running that configuration. That description contains information not
in the Installation and System Administration Guide.

Additional notes

Additional information about using this release — and which is not included in the documentation
— can be found in “Tips for using One-To-One Enterprise” on page 22 and “Supplemental
documentation” on page 25 of this document.

Migration notes

The instructions for migrating your Version 3.0 One-To-One installation to this version are
documented in the Installation and System Administration Guide. See that manual for details. Also,
review “What’s new or changed in Version 4.1” on page 7 of this document to be aware of changes
to the system or conﬁguration that might affect this migration.

Additionally, be aware of these issues:

Version 3.0 user name conﬂicts

Migrating Version 3.0 One-To-One Command Center user names to Version 4.1 might change the
user names. In Version 3.0, the Command Center user information was stored in a ﬁle separate from
the One-To-One accounts and users tables. These have been combined in Version 4.1. As such, when
the Version 3.0 data contains One-To-One Command Center users and registered application users
with the same name, the duplicate Command Center names will be altered to end in a numeral. For
example, if both Version 3.0 ﬁles contain users named “Nancy”, one of the account names will be
“Nancy” and the other will be “Nancy1”. When this happens, the dbmigrate sub-utility logs an
error to the bvlog ﬁle: the log message contains text that states that there was a user with an
existing name. See the Command Center User’s Guide for information about changing Command
Center user names.

Gateway modules

This release provides new gateway modules that incorporate improved error checking and security.

On each HTTPD machine, replace the original gateway with the new one provided in this release,
and then restart the HTTP server. The gateways are: anamecgi.exe, inetcgi.exe, and
bvisapi.dll. If you have a named gateway, be sure to replace the gateway ﬁle, and rename the
new ﬁle to the gateway name. Consult the Installation and System Administration Guide for details.

BroadVision, Inc.

290-41A-NAS

One-To-One Server Release and Installation Notes

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Installing One-To-One Version 4.1

17

Switching database vendors

If you are migrating from an older version and switching your database vendor (such as SQL Server
to Oracle), remove BV_DB_LIB, BV_DB_TYPE, and BV_DB_BASE from the system’s environment
variables before installing and conﬁguring One-To-One. They are no longer used and their presence
might cause problems.

One-To-One Server Release and Installation Notes

290-41A-NAS

BroadVision, Inc.

18

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Problems fixed in the Version 4.1 release

Problems fixed in the Version 4.1 release

The following problems were ﬁxed in the Version 4.1 release:

Database issues

l 04029: Running the install_observe_db utility generates numerous SQL usage errors when

you run it with no arguments and the $BV_DB_PASSWORD variable is not set.

l 05792: When a content item is modiﬁed from a script or dynamic object, a query that is based on
some attribute value of contents might still have the old item in the content list. This includes
the visitor feedback (voting) of content ratings.

l 06216: If you have privacy_flag set in the bv1to1.conf ﬁle, it must be set to zero.

Server and environment issues

l 04179: BV_SessionClt::srep_get_destinations() does not retrieve the visitor’s e-mail

and phone information.

l 04722: BV_ContentDB::delete_content_by_list() incorrectly deletes all incentives and

does not return error when deleting an incentive that should not be deleted, such as one that is
on-line, or which has a coupon that has been distributed.

l 06628: In this release, the bvsystemd socket BACKLOG is set to 1024 calls in the queue.

l 07096: Installing and uninstalling Orbix requires manually running the orbixds utility.

l 07907: The system portal — system() — does not strip trailing line terminator, and the <CR>

character becomes part of the command, which typically causes the command to fail.
Workaround: Remove unwanted <CR> characters using this script:

cmd = ....;
cmd = cmd.replace(/\r/g, "");

Known One-To-One problems, and issues

Please note the following One-To-One problems, and issues:

Installation and System Administration Guide

l When setting up a notiﬁcation system, it is important to put sched_header.jsp in the

bv_schedule_script_root directory. There is a default copy in $BV1TO1/lib/. Customize
this ﬁle if you implement a custom delivery method.

l 07659: The Notiﬁcations delivery server has two additional parameters that are not documented
and which control how many messages to send at a time, and how long to wait before sending
the next set. See “Notiﬁcations handler changes” on page 10 for details.

l 08320: The address for BroadVision Europe, on the back cover of the manual, is incorrect. The

correct address is:

BroadVision Europe
Fiechthagstrasse 4
4103 Bottmingen
Switzerland

BroadVision, Inc.

290-41A-NAS

One-To-One Server Release and Installation Notes

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Known One-To-One problems, and issues

19

Developer’s Guide to Components and Scripts

l The BVI_NamingContext component is not usable with servers that communicate via IIOP

because Orbix 2.2 on Windows NT does not have support for IIOP.

API Reference

Installation issues

l 07542: Several times the manual references the “Orbix Programmer’s Guide”. That is the old
name for the manual. It should be the “Orbix Programming Guide”, which is provided in the
$BV1TO1/orbix/doc directory.

l 07794: The installation program creates a program folder called “BroadVision One-To-One 4.1
Enterprise” and which provides ﬁve shortcuts for the default instance and default application.
Each of the shortcuts is missing a semi-colon (;) in its short-cut. Here are the descriptions of the
short-cuts and the correct short-cut paths, you can correct them from the Properties dialog of
each short-cut in the C:\WINNT\Profiles\All Users\Start
Menu\Programs\BroadVision One-To-One 4.1 Enterprise folder:

• bv1to1 sh — Launches a MKS Korn Shell. This short-cut has no errors.

• Restart One-To-One Servers — Restarts the default instance of the One-To-One servers. The

missing semi-colon appears ﬁrst in this example:

sh.exe -c "echo 'Restarting One-To-One Servers...\n'; ...

• Shutdown One-To-One Servers — Stops the default instance of the One-To-One servers. The

missing semi-colon appears ﬁrst in this example:

sh.exe -c "echo 'Shutting down One-To-To Servers...\n'; ...

• Start Interaction Manager — Starts the default Interaction Manager. The missing semi-colon

appears ﬁrst in this example:

sh.exe -c "echo 'Starting Interaction Manager...\n'; ...

• Stop Interaction Manager — Stops the default Interaction Manager. The missing semi-colon

appears ﬁrst in this example:

sh.exe -c "echo 'Stopping Interaction Manager...\n'; ...

To create short-cuts that operate on non-default servers and Interaction Managers, deﬁne the
system environment variables in the short-cut command. For example, to restart the servers
with a different $BV1TO1_VAR and $BV1TO1_INSTANCE:

sh.exe -c "BV1TO1=d:/bv1to1 BV1TO1_VAR=c:/abc_var BV1TO1_INSTANCE=abc
c:/bv1to1/bin/bvconf restart; echo ’Enter\c’; read x"

Interaction Manager issues

l 02845: Reducing the count of Interaction Manager engines using the imgr_conf utility does
not reduce the count in the namespace until all Interaction Manager and One-To-One servers
are restarted. This has the side-effect that when the One-To-One Command Center or
cache_util utility ﬂushes caches, the Interaction Manager engines might unexpectedly be
restarted.

One-To-One Server Release and Installation Notes

290-41A-NAS

BroadVision, Inc.

20

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Known One-To-One problems, and issues

Database issues

Third party issues

l 06456: The Schema generator does not generate an error when two content types have the same

table name.

l 03797: The AOL 3.01 browser version 3.01 — “Mozilla/2.0 (Compatible; AOL-IWENG

3.0; Win16)” — does not return all the information necessary to identify the visitor’s request.
Workaround: visitors using AOL browsers must upgrade to a later version or use a different
browser.

l 03867: RogueWave does not catch invalid dates, such as 02/35/98. This often does not become
apparent until the DBMS generates an error, which then gets written to the bvlog.out ﬁle. For
example:

L1:S05 bv_db_ex_handler:[SERVERERROR] Error from Server: ORA-0 1843:
not a valid month, errnum=1843, severity=0, msg1=brisk

l 05720: Microsoft Internet Explorer version 3 (IE3) sometimes fails to properly refresh pages.
(This does not happen in IE4 or Netscape 4.) When this occurs, the Interaction Manager
determines that there is an access control violation and logs errors similar to this:

L1:S18 BVSM_PathValidator::compute_path: User -148 is not allowed to
access subject ’broadway/scripts/registered/bw_acct.jsp’
L1:S18 BVSM_JSPTask::validate: path validation failed for
/broadway/scripts/registered/bw_acct.jsp
L1:S18 Error on process_cgi (stream)

l 07263: The CashRegister 2.X is no longer available from CyberCash. If you have a license and
need the software, contact BroadVision Customer Support. See “Technical support” on page 3
for details.

Script and component issues

l 04188: Calling setType() on a type on BVC_Value component is problematic. For example,

setType(BVC_String_Type) on a BVC_Value and then calling setStringValue() causes
setStringValue() to delete the previously allocated string.
Workaround: don’t use setType().

l 07102: content: BVI_Value assumes that strings beginning with zero (0) are octal when

converting to numeric. This happens because BVC_Value uses strtol() to convert strings to
numbers, and that function assumes that strings with leading zeros are octal numbers. As a
result, 8 and 9 are invalid octal digits, strtol() stops after the “0” when scanning “08” and
“09”; “08” returns 0, not 8. Note that this is true for Javascript too: parseInt("08") returns 0,
not 8.

l 07177: component: get_session_id() sometimes returns invalid data.

Workaround: Replace the get_session_id() call with get_BV_SessionID(). See “Session
client tips” on page 24 for more information.

Matching Agent issues

l 04184: The Matching Agent generates an incorrect query when the matching rule includes an

attribute not in the visitor proﬁle. It should generate an error. For example, if the rule is
PRICE user.PRICE, and PRICE is not a visitor attribute, the system looks for PRICE = -1.

BroadVision, Inc.

290-41A-NAS

One-To-One Server Release and Installation Notes

Server and environment issues

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Known One-To-One problems, and issues

21

l 02397: In the bv1to1.conf ﬁle, service names must be deﬁned with single-byte characters and

no whitespace.

l 05804: The following log message is the result of a problem with the Orbix name server. You can

ignore errors similar to this:

L1:S07 NamingContext:marker <0> does not match <NC#33-904699543>

l 05998: Using the Command Center to move a new content item to a category from an off-line

category writes an error to the log ﬁle because the One-To-One Command Center tries to ﬂush it
from the content cache, but the category does not yet exist in the cache. The error looks like this:

L1 error in log "Error on flush_on_content" - failed to get
category with OID -4123

l 06746: When migrating a One-To-One system using the Oracle DBMS, bvconf execute

reports that it is adding stores and that they already exist. It also generates L1 errors in the log
ﬁle similar to the errors shown here. You can safely ignore these errors.

BV1TO1 ; $BV1TO1_VAR
data dependencies: migration
error from logfile:

...db_init...Error from Server: ORA-00001: unique constraint
(QATEST3.BV_ADMIN_USER_IND) violated,
errnum=1, severity=0 , msg1=rogue

...db_init...db_init:BV_StoreDBA::_insert_adm_user_tbl:
trying to insert a new row with duplicate value.

...db_init...BV_StoreDBA::_process_command:AddStoreCmd:
store SuperDuperBooks exists.

l 08153: The ﬁrst time you create alerts, the system generates the errors, “Cannot ﬁnd function

‘bvfn_balance_alert_init’ for alert_type ‘bvfn_balance_alert’ in the shared library
‘libalert_ext.dll’ and “Error while registering plug-in function ‘bvfn_balance_alert’ for
alert_type ‘bvfn_balance_alert’.”

l 08202: The Notiﬁcations sched_srv server doesn’t call init function for C++ alert plug-ins.

Attempting to initialize such a plug-in typically causes an access violation and a termination.

l 08208: In the matching sample, the matching.dsp ﬁle builds a ﬁle called libmatching.dll.

To work correctly with the system, though, it should be named libmatch_ext.dll.
Workaround: rename the generated ﬁle and copy it to $BV1TO1/bin.

l 08225: The match_func_gen sample utility generates a initialization function

bv_init_matching_extensions() that is not declared for DLL export. As a result, the function is
not visible to other programs (such as the Interaction Manager).

l 08228: The bv1to1.conf ﬁle does not contain a deﬁnition for the AVPIN export variable used
by the AVP Taxing system. This variable must be deﬁned when performing any operations
through the One-To-One taxing servers. To deﬁne this variable, add it to the “Export” section of
bv1to1.conf and assign one (1) to its value.

AVPIN="1"

l 08256: The Alerts sample program has these errors:

One-To-One Server Release and Installation Notes

290-41A-NAS

BroadVision, Inc.

22

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Tips for using One-To-One Enterprise

• The sample builds libalert.dll, which conﬂicts with the one of the same name in

already $BV1TO1/bin.

• The shared libraries that contain the sample C++ plug-ins, as speciﬁed in

alert_type_spec.src (LIB_NAME), have the UNIX names libbalance.so and
libproduct.so. Also, the sample builds just one library, libalerts.dll, which does not
demonstrate the multiple library approach discussed in the readme ﬁle. And the .dmp ﬁle
as generated from the .src ﬁle contains an invalid LIB_NAME.

• The .dsp ﬁle refers to many header ﬁles in "..\..\..\thirdparty\root\include", which is not

correct for your build environment.

l 08266: When the ext_lib parameter is deﬁned, the external database accessor (extdbacc_ fails

to start. The error is revealed by this error message in the log ﬁle:

BV_ExtDBAccHook::post_activate(): fail to load shared lib xxxx
WIN32 Error: LoadLibrary Cannot create a file when that file
already exits.

One-To-One Design Center

l 06018: The One-To-One Design Center stalls for several minutes after choosing File|Export

To|Server Codeset Format... when there is no service host set.

BroadWay sample application

l 06050: The Broadway sample application’s bw_acct.jsp fails if you try to set the same

account information twice. This happens because the script tries to enter duplicate entries in the
database, and setProperty() correctly sets an error, but there is no error page to process the
error, so the script stops immediately.

l 07532: Installing the One-To-One Enterprise Broadway sample application after installing a
BroadVision One-To-One application (such as One-To-One Publishing Center, One-To-One
Commerce, One-To-One Financial, or One-To-One Knowledge) will corrupt the Broadway
sample data.
Workaround: Install the Broadway sample before installing a One-To-One application.

Tips for using One-To-One Enterprise

This section describes tips for using the One-To-One system.

Server tips

l If the Notiﬁcation system sched_srv crashes during a job, the sched_poll_d server does not
pick up this job to process because the database entry for this job is in a transient stage. To start
the process again, you must stop and restart the server with these commands:

bvconf shutdown -d sched_poll_d
bvconf restart -d sched_poll_d

Alternately, you can use the One-To-One Command Center to modify the schedule. This has the
added beneﬁt of cleaning the database.

BroadVision, Inc.

290-41A-NAS

One-To-One Server Release and Installation Notes

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Tips for using One-To-One Enterprise

23

l When you create a list object, be sure to set its length before passing it to the servers; otherwise,

the list length defaults to zero (0). For example,

BV_ProfAttrValueList value_list;
value_list.length(2);

On a related note, declare maximum length when you create the list — this allocates enough
memory to contain the elements. Then, as long as you do not exceed the length when
populating the list, you will not re-allocate the buffer each time you add an item. For example:

BV_ProfAttrValueList value_list(N);
CORBA:ULong i = 0;

while (...) {

value_list.length(i + 1);
value_list[i] = ...;
++i;

}

// Whatever the loop condition is
// No buffer reallocation when i < N

l The taxing and shipping cost handlers that are provided with One-To-One are very

rudimentary. For example, the taxing system uses only a small subset of the AVP taxing
package’s capabilities, and the shipping system makes charges based on hard-coded
assumptions. If you are going to use either of these packages, you should implement new
servers and build them into the shared library.

You could also purchase the BroadVision One-To-One Commerce ™ product, which contains
more fully featured taxing and shipping functionality.

l Use the Windows NT Task Manager (TASKMGR.EXE) to identify running processes. If you are
sharing a machine with another person, use PVIEW.EXE (from the Windows NT Resource Kit)
to examine a process’s “token” to identify who owns the process.

l When implementing a shipping cost server, be sure to validate the destination addresses.

Various problems occur when invalid postal codes, addresses, and such are entered and then
the shipping implementation incorrectly handles the errors.

l Do not specify a creation time when inserting a product into the Product database with

insert_content(), the system automatically inserts the time. If you do specify a time, the
system ignores it and no error or warning occurs.

l One-To-One doesn’t use concurrent order fulﬁllment back-end processes.

Workaround: For a large site with many services, group the services in subgroups. Each group
can have its own dedicated fulﬁllment back end shared by services within the same group.

l Changes to the Matching system meta rules are not accepted during a visitor’s session.

Workaround: Visitors must re-login to have the new rules take effect.

l The SalesRep does not guarantee to return the “best” — for buyer or seller — discount. For

example, in an incentive with details like “Buy 2, get 50% discount on next 1”, the 50% discount
might be interpreted to apply to either a second item of equal or lesser value. However, the
SalesRep can allow the second item to be of greater value.

l BVRT_Value::as_string() returns dates formatted to correspond to the operating system
LC_TIME locale rules. By default, the operating system returns 2-digit year values; the default
time locale, date format is deﬁned to be %m/%d/%y, which returns a date formatted like,
03/15/99. If you want a four-digit year, change your time locale to use uppercase ‘Y’ for the
year: %m/%d/%Y returns 03/15/1999. See the setlocale and strftime man pages for details.

One-To-One Server Release and Installation Notes

290-41A-NAS

BroadVision, Inc.

24

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Tips for using One-To-One Enterprise

Interaction Manager tips

l When debugging Dynamic Objects, core ﬁles for the Interaction Manager servers are written to:

$BV1TO1_VAR/BVSNsmgr/<host name>/logs/

l When the Interaction Manager fails to load a component or dynamic object library, it is usually
because the library ﬁle is not in the search path. On Windows NT, use DEPEND.EXE (from the
Windows NT Resource Kit) to identify this problem.

l If the Interaction Manager does not shut down cleanly, it sometimes leaves system portal

daemons (bvsystemd) running. You can safely shut these down manually.

l Special HTML characters — such as an ampersand (“&”) — might not display correctly in the

Netscape Navigator browser when contained in content names.

l Users of Microsoft Internet Explorer version 2.0, and some of the version 3.x, cannot leave a
BroadVision One-To-One site, and then use the browser’s “Back” button to return to the
One-To-One site’s Web page.
Workaround: Use a newer version of Internet Explorer.

Session client tips

BV_SessionClt contains two methods that should not be confused:

l get_session_id() returns a pointer to a STRING that contains a representation of the

internal session ID which is a randomly generated LONG.

l get_BV_SessionID() returns a pointer to a STRING that contains a representation of the
internal session ID followed by a dot and then a timestamp. This format is conﬁgurable.

Dynamic object tips

l When using Dyn_IOField and the ﬁeld value is an image, specify the default text for the value
attribute to avoid problems with Microsoft Internet Explorer 3.0 referencing empty images.

l When debugging messages are turned on, truncate the message log periodically; the ﬁles grow

quite large very rapidly.

Database tips

Browser tips

l Do not create Content attribute names that contain hyphens (-). This does not apply to “friendly

name” values which can have hyphens.

l The incentive system requires the presence of the BV_INCENTIVE_PROGRAM table; this table

cannot be renamed.

l If you are using SQL Server, the One-To-One database user account must have permission to

truncate the database log.

l Cutting and pasting in Japanese Windows browsers into hidden password ﬁelds does not retain
the correct character encoding, which causes an error when the Interaction Manager retrieves
the data. This has been observed on both Netscape and Microsoft browsers
Workaround: Enter the characters manually instead of copy and pasting them.

l Using Microsoft Internet Explorer on a system where Netscape is conﬁgured as the default

browser may cause unexpected “File not found” errors when Java Scripts on page templates
attempt to open ﬁles passed from the Interaction Manager. You can safely close the error dialog
with no ill effects.

BroadVision, Inc.

290-41A-NAS

One-To-One Server Release and Installation Notes

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Supplemental documentation

25

Supplemental documentation

Here is some additional information not included in the One-To-One documentation:

l “Accessing properties with BVI_Properties” on page 25

l “Cheap sessions and BV_SmgrSessionHandle” on page 26

l “Clariﬁcation of system() command examples” on page 27

l “Loading observations to Oracle across platforms” on page 27

l “Running HTTP on a machine different from the Interaction Manager host” on page 28

Accessing properties with BVI_Properties

The BVI_Properties interface supports two different ways to store and retrieve properties. The two
ways cannot, in general, be intermixed.

The ﬁrst method is the explicit API. From the JavaScript interface,

interface BVI_Properties {

...
BVI_Value get(string key);
long set(string key, BVI_Value value);
...

}

Using the get() and set() API, you construct a BVI_Value to pass to get(). When later retrieved by
set(), there is a different JavaScript object created, but the component it references is identical to that
of the argument passed to set(). In particular, the retrieved value is still of type BVI_Value. This is
the only way that enumerated and dictionary types can be stored as units; of course, you can always
store their more primitive parts via either method.

When using the dynamic properties API, you can pass any JavaScript non-object type (string,
number, boolean), or a JavaScript object that refers to a component. Internally, these are held in a
hash table of BVC_Values, so whatever the incoming argument is to a property store, it gets
wrapped in a BVC_Value for storage. When later retrieved, the value gets taken out of the
BVC_Value, and converted to the appropriate JavaScript type for return to the script.

On the other hand, the get() API takes the same BVC_Value and wraps a BVI_Value reference
around it for return to the script. So, if a hash table entry is a BVC_Value instance containing a
string, when it is retrieved through get(), the result is a BVI_Value that contains a copy of the
BVC_Value, containing a copy of the string; when retrieved through the dynamic properties
interface (the natural JavaScript property syntax), the string itself is returned.

Do not intermix the two methods; it will produce incorrect results. Either always store and retrieve
through the dynamic properties API, or always store and retrieve through the get() or set() API,
depending on your application needs.

One-To-One Server Release and Installation Notes

290-41A-NAS

BroadVision, Inc.

26

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Supplemental documentation

On a related note, BVI_Value (and BVC_Value) support both enum types and dict types, in the sense
that these types are deﬁned in the BroadVision database schema. However, it is not possible to
assign values of either of these types directly to a BVI_Value, unless the BVI_Value already holds
that type. This is because it is impossible to determine from a string which enum or dict type you are
referring to. So, this code will fail at the second line:

var value = new BVI_Value();
value.enumValue = '15-17';

The right way to do this is to initialize and assign with either the setEnumValue or setDictValue
method.

var value = new BVI_Value();
value.setEnumValue('15-17', 'AGE_RANGE');

You can then assign another element of the same enumeration directly:

value.enumValue = '18-24';

Cheap sessions and BV_SmgrSessionHandle

To conserve Interaction Manager resources, when the ﬁrst response page in a session does not
contain session information (BV_SessionID and BV_EngineID), the session is immediately garbage-
collected after the page is sent. Because there is no session information in the response page, there is
no way for the browser to get back to the session. This is called a cheap session.

The way that BV_SmgrSessionHandle works with sessions conforms to this behavior. If the output
from the ﬁrst call() function on a BV_SmgrSessionHandle object contains session information,
that information is stored internally by the BV_SmgrSessionHandle object. If the output of the ﬁrst
call() function does not contain session information, then that session is considered a cheap
session, no information is stored, and the socket connection to the Interaction Manager is released.
In this latter case, a call to get_session_id() returns a NULL (0) pointer.

Any subsequent call() function causes the BV_SmgrSessionHandle object to establish a new
socket connection to another Interaction Manager, which then creates a new session to execute the
passed-in page script. (It is possible that the Interaction Manager could be the same one as for the
previous call, but not likely.)

If you want a series of call() functions to use the same session, then the ﬁrst response page must
return session information. Regardless of whether a session is a “cheap” session or not, the same
BV_SmgrSessionHandle object can pass in multiple call() functions to an Interaction Manager;
each page script just executes in a different session that may or may not be created by the same
Interaction Manager.

BroadVision, Inc.

290-41A-NAS

One-To-One Server Release and Installation Notes

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Supplemental documentation

27

Clariﬁcation of system() command examples

This example runs the word count utility and displays “1 1 4”. Because of the implementation for
strings, the count of characters in “123” is four. In this example, ‘123’ is passed to the word count
utility as stdin.

Response.write(system('wc', '123');

Equivalent UNIX command line:

echo 123 | wc

This example calls system() from within a JavaScript function to dump a ﬁle. In this example,
ﬁlename is included in the ﬁrst parameter to system() and becomes one of the command line
parameters.

// read a file into a string
function readfile(filename) {

return system("cat -s -n " + filename); }

Equivalent UNIX command line:

cat -s -n filename

Loading observations to Oracle across platforms

The control ﬁles (.ctl) that come with One-To-One, and which are used to tell Oracle how to load
observation data, are not intended to be used across platforms, such as when the Oracle server is
running on UNIX. The control ﬁles use “direct” mode, which is the fastest way to load data into the
database. However, when using this mode across platforms, the “unrecoverable” option — which is
speciﬁed in the control ﬁles — is not available. As such, if you are using Oracle across platforms,
you need to edit the control ﬁles and remove the UNRECOVERABLE option that appears in the ﬁrst
line of each of these ﬁles:

buy.ctl
choose.ctl
end_sess.ctl
enter_sess.ctl
enter_store.ctl
identify.ctl
see.ctl
see_ad.ctl
select.ctl
select_ad.ctl
target_rule.ctl

To correct the ﬁles, copy them $BV1TO1/bin/scripts to a local directory, and edit the copied
ﬁles. Then, to use these ﬁle, disable “direct” mode when you run the obs_load utility:

obs_load -log_date <date> -direct_mode_flag_for_oracle false

One-To-One Server Release and Installation Notes

290-41A-NAS

BroadVision, Inc.

28

BroadVision One-To-One Version 4.1 for Windows NT Server Release Notes
Supplemental documentation

Running HTTP on a machine different from the Interaction Manager host

If your HTTP server is running on a host separate from the one running the Interaction Manager
servers:

1. Determine the location where you want the conﬁguration ﬁle to be located on the HTTP host
machine. This is a directory that you create, for example, d:\BVSNsmgr\ is a good location.

2. Copy the conﬁguration ﬁle from the default location to the directory on the HTTP host.

When you conﬁgured the Interaction Manager servers, that process created a bvsm.cfg
conﬁguration ﬁle in $BV1TO1_VAR/BVSNsmgr/. If you named your application, the ﬁle is
“appname.cfg”. Copy that ﬁle from the Interaction Manager host to the new directory on the
HTTP host.

3. Create two registry keys on the HTTP host (run the Windows NT regedit utility):

a. If this registry path does not already exist, create it:

\HKEY_LOCAL_MACHINE\SOFTWARE\BroadVision\

One-To-One Application System\4.1\Interaction Manager\
default\export\

If you are using a named application, replace “default” with the name, such as “appname”.

b. Create the BV1TO1_SESSION_CFG key, and enter the location you created in Step 1, such as

d:\BVSNsmgr\

c. Create the BVSNSMGR_LOGS key and enter the same location. (You may choose another

location.) This is where the gateway application writes it’s log ﬁles.

You can now connect to a Interaction Manager server running on a different machine.

BroadVision, Inc.

290-41A-NAS

One-To-One Server Release and Installation Notes

