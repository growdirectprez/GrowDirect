---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/SWINDON/Release Notes/Enterprise 4.1 NT release notes.pdf.md
tags: [retail, pwc, swindon, sap-retail, broadvision, coe, 1999]
project: retail
status: unprocessed
---

# Enterprise 4.1 NT release notes.pdf

## Source
File: `Brain/raw/.extract/SWINDON/Release Notes/Enterprise 4.1 NT release notes.pdf.md`
Size: 68,080 bytes

## Raw content
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

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
