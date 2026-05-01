BroadVision®

One-To-One™

Enterprise

Installation and

Administration Guide

Version 4.1

BroadVision,® Inc.
585 Broadway
Redwood City, CA 94063
(650) 261-5100

234-410-SAB

Installation and Administration Guide

Copyright © 1995-1999 BroadVision, Inc. All rights reserved.
585 Broadway, Redwood City, California 94063 U.S.A.
Printed in the United States of America

This manual and the software described in it are copyrighted.
Under the copyright laws, this manual or the software may not be copied, in whole or in part,
without prior written consent of BroadVision, Inc. or its assignees, except for purposes of internal
use by licensed customers of BroadVision. This manual and the software described in it are provided
under the terms of a license between BroadVision and the recipient, and their use is subject to the
terms of that license.

RESTRICTED RIGHTS LEGEND: Use, duplication, or disclosure by the government is subject to
restrictions as set forth in subparagraph (c)(l)(ii) of the Rights in Technical Data and Computer
Software clause at DFARS 252.227-7013 and FAR 52.227-19.

The product described in this manual may be protected by one or more U.S. and International
patents. The BroadVision One-To-One software is covered by U.S. patent 5,710,887.

DISCLAIMER: BroadVision, Inc. makes no representations or warranties with respect to the contents
or use of this publication. Further, BroadVision, Inc. reserves the right to revise this publication and
to make changes in its contents at any time, without obligation to notify any person or entity of such
revisions or changes.

TRADEMARKS: BroadVision and the BroadVision logo are trademarks or registered trademarks of
BroadVision, Inc. in the United States and other countries. BroadVision One-To-One, One-To-One
Enterprise, One-To-One Commerce, One-To-One Applications, One-To-One Command Center,
One-To-One Publishing Center, One-To-One Knowledge, One-To-One Financial, One-To-One Design
Center, One-To-One Instant Publisher, One-To-One System Manager, and One-To-One Tools are
trademarks of BroadVision, Inc.

IONA and Orbix are trademarks of IONA Technologies, Ltd.
RSA, MD5, and RC2 are trademarks of RSA Data Security, Inc.
Rogue Wave, .h++, Tools.h++, and DBtools.h++ are trademarks of Rogue Wave Software, Inc.
Verity, Topic, and SEARCH’97 are trademarks of Verity, Inc.
Acrobat and the Acrobat logo are trademarks of Adobe Systems Incorporated.

All other trademarks, service marks, and trade names belong to their respective owners. BroadVision, Inc.
disclaims any proprietary interest in the marks and names of others.

Contains security software from RSA Data Security, Inc.
This version supports international security with RC2 and MD5.

BroadVision, Inc.

revised summer 1999

Contents

iii

Preface
ix
Related documents ......................................................................................................................................x
Technical Support .......................................................................................................................................xi
Typographical conventions .......................................................................................................................xi

1 Introduction

1
Conﬁguration concepts and terminology ................................................................................................ 4

2 Installation

7
Prerequisites ................................................................................................................................................. 8
Installing One-To-One ............................................................................................................................... 10
Installing One-To-One on Solaris ............................................................................................. 10
Installing One-To-One on HP-UX ............................................................................................ 12
Installing One-To-One on Windows NT ................................................................................. 14
Removing the One-To-One Enterprise software ................................................................................... 15
Removing a Windows NT installation ..................................................................... 15
Removing a UNIX installation .................................................................................. 15

3 Upgrading to Version 4.1

17
Old system .................................................................................................................... 18
New system .................................................................................................................. 18
Migration prerequisites ............................................................................................................................. 19
Replicating directories and conﬁguration ﬁles ...................................................................................... 20
Migrating the database schema ............................................................................................................... 21
Migrating system conﬁguration .............................................................................................................. 23
Updating Version 4.0 scripts .................................................................................................................... 27
Updating components and dynamic objects ......................................................................................... 28

Installation and Administration Guide

BroadVision, Inc.

iv

Contents

4 Setup

29
Overview .................................................................................................................................................... 30
Conﬁguring and starting the One-To-One servers ............................................................................... 31
Deﬁning system environment variables ................................................................................. 31
One-To-One variables ................................................................................................. 32
Database variables ...................................................................................................... 33
Oracle variables ........................................................................................................... 33
Sybase variables .......................................................................................................... 35
SQL Server variables .................................................................................................. 35
Informix variables ....................................................................................................... 36
Conﬁguring the One-To-One environment and services ..................................................... 37
Starting the One-To-One servers .............................................................................................. 38
Shell start-up scripts ................................................................................................... 39
Conﬁguring and starting the Interaction Manager .............................................................................. 40
Conﬁguring the Interaction Manager server ......................................................................... 40
Starting the Interaction Manager ............................................................................................. 42
Conﬁguring the HTTP server .................................................................................................................. 43
Conﬁguring the gateway for Netscape Enterprise Server (NES) ........................................ 44
Conﬁguring the gateway for Microsoft Internet Information Server (IIS) ........................ 46
Conﬁguring the gateway for a standard CGI server ............................................................ 48
Troubleshooting Interaction Manager start-up problems .................................................... 49
Conﬁguring the Broadway sample application ..................................................................... 50

5 Server configuration

53
Naming your site and default service .................................................................................................... 54
Adding, changing or removing a service .............................................................................................. 54
Changing the “Unclassiﬁed” content label ........................................................................................... 54
Conﬁguring access control ....................................................................................................................... 55
Conﬁguring caching ................................................................................................................................. 58
Setting the Year 2000 cut-off date ............................................................................................................ 61
Conﬁguring locales ................................................................................................................................... 62
Character sets .............................................................................................................................. 65
Conﬁguring database accessors .............................................................................................................. 66
Conﬁguring visitor notiﬁcations ............................................................................................................. 69
Notiﬁcation process ................................................................................................................... 70
Message scripts ........................................................................................................................... 73
Messages ...................................................................................................................................... 73
Processes and daemons ............................................................................................................. 74
sched_poll_d ................................................................................................................ 74
sched_srv ...................................................................................................................... 75
deliv_smtp_d ............................................................................................................... 76
deliv_comp_d .............................................................................................................. 78
Deﬁning session proﬁle terms ................................................................................................................. 78
Conﬁguring observation logging ............................................................................................................ 80
Conﬁguring the Matching Agent ............................................................................................................ 81
Content rating values ................................................................................................................ 81
Scoring ......................................................................................................................................... 82
Rankings and cutoffs ................................................................................................................. 83
Content order .............................................................................................................................. 84
Adding an input argument to the Matching Agent ............................................................................. 85
Setting matching and pricing rule evaluation time .............................................................................. 86
Using the Verity search engine ................................................................................................................ 86
Conﬁguring One-To-One for Verity ........................................................................................ 87
Identifying what to index ......................................................................................................... 87
Creating a search collection ...................................................................................................... 89
Maintaining up-to-date Verity collections .............................................................................. 91

BroadVision, Inc.

Installation and Administration Guide

Contents

v

Changing the site ID ..................................................................................................................................91
Running multiple One-To-One servers on one host .............................................................................92
Running a multiple-host conﬁguration ..................................................................................................93
Running a multiple-site conﬁguration ....................................................................................................95
Conﬁguring a multiple-site system ..........................................................................................97
Updating name space objects across sites ...............................................................................98
Coordinating operations ............................................................................................................99

6 Interaction Manager configuration

101
HTTP servers and the Interaction Manager .........................................................................................102
Directories and URLs ................................................................................................................103
Named applications ..................................................................................................................104
Gateway applications ...............................................................................................................105
Gateways and session IDs .......................................................................................................106
Firewalls .....................................................................................................................................106
Ports and IP addresses ..............................................................................................................108
Conﬁguring the host machines ................................................................................110
Conﬁguring IP masking for proxy servers ........................................................................................... 111
Running multiple applications on a single CGI host .......................................................................... 111
Using SSL with Netscape HTTP servers ...............................................................................................112
Customizing the session ID format .......................................................................................................112
Conﬁguring the page request cache ......................................................................................................113
Using the cache conﬁguration ﬁle ..........................................................................................114
Cache settings .............................................................................................................114
Cache list .....................................................................................................................115
Fix up scripts ...............................................................................................................115
Cache rules ..................................................................................................................117
Cache rule syntax .......................................................................................................118
Cache name .................................................................................................................121
Changing the request cache dynamically ..............................................................................121
Monitoring cache status ...........................................................................................................122

7 Commerce-specific configuration

123
Installing AVP Taxware ...........................................................................................................................124
Conﬁguring the Taxing system ..............................................................................................................126
Computing Shipping Costs ....................................................................................................................127
Conﬁguring order numbers ....................................................................................................................128
Conﬁguring microtransaction logging ..................................................................................................129
Conﬁguring payment handling .............................................................................................................130
Conﬁguring payment types .....................................................................................................131
Conﬁguring payment handlers ...............................................................................................131
Obtaining billing addresses ......................................................................................131
Conﬁguring payment methods ................................................................................132
Conﬁguring payment daemons ...............................................................................132
Conﬁguring payment logging .................................................................................................135
Conﬁguring Omnihost (Solaris only) .....................................................................................135

Installation and Administration Guide

BroadVision, Inc.

vi

Contents

8 Maintenance

137
Shutting down your site ......................................................................................................................... 138
Restarting your site ................................................................................................................................. 139
Recovering after a crash ......................................................................................................................... 140
Backing up your site ................................................................................................................ 141
Maintaining a stand-by server ............................................................................................... 142
One-To-One server machine crash ........................................................................................ 143
One-To-One unexpected behavior ......................................................................................... 143
Database server crash .............................................................................................................. 143
Database corruption ................................................................................................................ 144
Omnihost server machine crash ............................................................................................. 144
Monitoring server statistics ................................................................................................................... 145
Tuning for performance .......................................................................................................................... 149
Hardware conﬁguration .......................................................................................................... 150
Solaris machine conﬁgurations ............................................................................... 151
Tuning Interaction Managers ................................................................................................. 151
Tuning HTTP servers ............................................................................................................... 152
Netscape Enterprise Server ..................................................................................... 152
Tuning One-To-One server processes .................................................................................... 153
Maintaining Interaction Managers ....................................................................................................... 154
Using Interaction Manager log ﬁles ...................................................................................... 154
Monitoring for dead Interaction Manager servers .............................................................. 155
Purging discussion group messages .................................................................................................... 156
Determining software versions ............................................................................................................. 156

9 Utilities and other files

157
acltool ........................................................................................................................................................ 158
bounced_email_utl .................................................................................................................................. 160
bv1to1.conf ............................................................................................................................................... 161
Deﬁnitions ................................................................................................................................. 162
Export environment variables ................................................................................................ 163
Site conﬁguration ..................................................................................................................... 166
site ............................................................................................................................... 166
process ........................................................................................................................ 169
service ......................................................................................................................... 172
group ........................................................................................................................... 172
bvconf ........................................................................................................................................................ 174
dump .......................................................................................................................................... 175
execute ....................................................................................................................................... 175
help ............................................................................................................................................. 177
monitor ...................................................................................................................................... 177
ns ................................................................................................................................................. 177
ping ............................................................................................................................................ 178
precheck ..................................................................................................................................... 179
ps ................................................................................................................................................ 179
restart ......................................................................................................................................... 181
shutdown ................................................................................................................................... 181
smap ........................................................................................................................................... 182
syntax_check ............................................................................................................................. 183
bvkill .......................................................................................................................................................... 183
bvlog .......................................................................................................................................................... 183
.bvlog.conf ................................................................................................................................................ 184
bvobs.conf ................................................................................................................................................. 187
bvping ....................................................................................................................................................... 188
bvsm.ACL ................................................................................................................................................. 189
bvsm.cfg .................................................................................................................................................... 190

BroadVision, Inc.

Installation and Administration Guide

Contents

vii

bvsm.req ....................................................................................................................................................191
bvsm_version ............................................................................................................................................191
cache_utl ....................................................................................................................................................191
dump_taxon ..............................................................................................................................................193
imgr_acltool ..............................................................................................................................................193
imgr_conf ...................................................................................................................................................194
indexer .......................................................................................................................................................195
load_data ...................................................................................................................................................197
migr_coll ....................................................................................................................................................197
migrate_to_v3.0 ........................................................................................................................................198
migrate_to_v4.0 ........................................................................................................................................198
migrate_to_v4.1 ........................................................................................................................................198
tmpl_mgr ...................................................................................................................................................198
watcher ......................................................................................................................................................200

A Component and dynamic object shared libraries on Solaris

Index

201

203

Installation and Administration Guide

BroadVision, Inc.

viii

Contents

BroadVision, Inc.

Installation and Administration Guide

Preface

ix

This guide describes how to install and conﬁgure the BroadVision® One-To-One™ application
system. To begin installing One-To-One, follow the instructions in Chapter 2, “Installation” on
page 7. The remainder of this guide discusses the following topics:

l Chapter 3, “Upgrading to Version 4.1,” explains how to migrate your existing system to Version

3.0.

l Chapter 4, “Setup,” describes how to setup and start a new One-To-One installation.

l Chapter 5, “Server conﬁguration,” details how to conﬁgure your One-To-One server system and

environment.

l Chapter 6, “Interaction Manager conﬁguration,” describes how to conﬁgure your Interaction

Manager and HTTP servers.

l Chapter 7, “Commerce-speciﬁc conﬁguration,” details how to conﬁgure the commerce features

of the BroadVision One-To-One Enterprise.

l Chapter 8, “Maintenance,” explains how to maintain your One-To-One system and

environment.

l Chapter 9, “Utilities and other ﬁles,” describes the tools, scripts, and support ﬁles used for

conﬁguring One-To-One.

l Appendix A, “Component and dynamic object shared libraries on Solaris,” describes Solaris

versioning of the Dynamic Object shared libraries.

This preface contains descriptions of the following topics:

l “Conﬁguration concepts and terminology,” next.

l “Related documents” on page x.

l “Technical Support” on page xi.

l “Typographical conventions” on page xi.

Installation and Administration Guide

BroadVision, Inc.

x

Preface
Related documents

Related documents

Documentation for the BroadVision One-To-One Enterprise is available electronically in HTML and
PDF formats. Additionally, two of the manuals, including this one, are also reproduced in print.
Additionally, the One-To-One Server Release Notes and One-To-One Command Center Release Notes are
only available in print.

On-line
documentation

To use the HTML or PDF documentation, you can either access it directly from one of the
CD-ROMs, or from the One-To-One system directory. In your browser, enter the URL that points to
the welcome.htm ﬁle.

If you are using the Application CD-ROM:

Platform

URL

Solaris
HP-UX 1
Windows 2

file:/cdrom/cdrom0/pubs/onetoone/welcome.htm

file:/cdrom/PUBS/ONETOONE/WELCOME.HTM

file:///E|/pubs/onetoone/welcome.htm

1 Some HP-UX CD-ROM drivers can’t resolve the HTML links. If you encounter this problem, copy the ﬁles to a hard disk.
2 This example assumes that the CD-ROM is in drive E:.

If you are using the Documentation CD-ROM:

Platform

URL

Solaris
HP-UX 1
Windows 2

file:/cdrom/cdrom0/welcome.htm

file:/cdrom/WELCOME.HTM

file:///E|/welcome.htm

1 Some HP-UX CD-ROM drivers cannot resolve the HTML links. If you encounter this problem, copy the ﬁles to a hard disk.
2 This example assumes that the CD-ROM is in drive E:.

If you are using the installed files, enter the full path to the installed ﬁle.

Platform
Solaris 1
HP-UX 1
Windows 2

URL

file:/opt/bv1to1/pubs/onetoone/welcome.htm

file:/opt/bv1to1/pubs/onetoone/WELCOME.HTM

file:///D|/bv1to1/pubs/onetoone/welcome.htm

1 $BV1TO1 is /opt/bv1to1.
2 $BV1TO1 is D:\bv1to1.

Optionally, you can copy or link the tree into the document root of your HTML server.

Additional BroadVision documents and white papers are available at:

http://www.broadvision.com

BroadVision, Inc.

Installation and Administration Guide

Preface
Technical Support

xi

Technical Support

If you have questions about the BroadVision One-To-One Enterprise or problems to report, please
contact the BroadVision technical support group by phone at 650-569-4333, or by e-mail at
bvhelp@broadvision.com.

BroadVision basic support services include telephone and electronic mail support from 9:00AM to
6:00PM PST/PDT on all business days. Basic support services are provided on an annual basis to
customers of BroadVision. A standard 90-day warranty is also provided with all software.

Typographical conventions

To distinguish sample code, commands, ﬁlenames, directory names, keywords, and syntax from
text, this manual uses the monospace font.

In command-line examples that you must enter, information that you must supply—and in which
the text shown is for example only—appears in monospace-italics. For example, in the
following command-line you must supply the value for the variable; the 1230 is for example only.

% setenv IT_DAEMON_PORT 1230

Note that system, subsystem, class, and member names are not called out in a different font.

Italics are for emphasis and to call out new terminology.

To distinguish pertinent information from the body text, this manual uses this icon.

Installation and Administration Guide

BroadVision, Inc.

xii

Preface
Typographical conventions

BroadVision, Inc.

Installation and Administration Guide

1 Introduction

1

A One-To-One site is a collection of software server processes running on one or more host
machines, connected to one or more databases, and has connections to Web browsers through a
network. While One-To-One, the Interaction Manager, and HTTP servers may all be installed on one
machine, this is not practical for most sites and applications.

Instead, the servers are distributed across several machines to balance the processing load, and to
provide security for your system. This diagram illustrates a possible large site conﬁguration.

HTTP/HTTPS
connections

TCP/IP
connections
through a ﬁrewall

CORBA (TCP/IP)
connections through
an optional ﬁrewall

CORBA
(TCP/IP)
connection

One-To-One
Command
Center

Browsers
connecting through
the Web.

Two HTTP servers
on two hosts.

Four Interaction
Manager engines
on three hosts.

One-To-One servers
on two hosts. Two
servers are database
accessors.

NFS
connections

How your site is conﬁgured depends on the expected trafﬁc volume, security requirements, and
hardware availability. The subsequent chapters in this manual provide the instructions for installing
the Interaction Manager software, and for conﬁguring and maintaining your site. If you are ready to
begin, start with Chapter 2, “Installation.” However, if you are not familiar with a One-To-One site
conﬁguration, review this chapter before you begin the procedure.

Installation and Administration Guide

BroadVision, Inc.

2

Chapter 1 Introduction

Once you have installed the software, you need to setup the system to start and run the One-To-One
and Interaction Manager servers. Chapter 4, “Setup,” describes the steps you need to perform to get
the system running. However, to conﬁgure speciﬁc parts of the system to your site’s needs, follow
the instructions in Chapter 5, “Server conﬁguration,” and Chapter 6, “Interaction Manager
conﬁguration.” If your site will be doing commerce activities, review Chapter 7, “Commerce-
speciﬁc conﬁguration.”

To keep your site running, tune it, or monitor the activity in the site, see Chapter 8, “Maintenance.”
Al of the scripts and utilities discussed in this manual are listed with usage information in Chapter
9, “Utilities and other ﬁles.

Directories and
ﬁles

The One-To-One system reads conﬁguration information from, and writes output ﬁles to, several
locations. However, most of these locations are subdirectories of one of these three locations:

l $BV1TO1 is the read-only directory where the One-To-One system ﬁles are installed. All

One-To-One and Interaction Manager executable and default conﬁguration ﬁles are located
under this directory, and all host machines must have access to this location. (This directory
may be replicated to multiple host machines, but this practice is not recommended. See
“Running a multiple-host conﬁguration” on page 93 for details.)

l $BV1TO1_VAR is a writable directory that contains the conﬁguration and system output ﬁles.
This directory is the “source of truth” for your site’s conﬁguration and parts of it should be
backed up regularly. [See “Backing up your site” on page 141.] All One-To-One and Interaction
Managerservers must have access to this location. (This directory may be replicated to multiple
host machines, but this practice is not recommended. See “Running a multiple-host
conﬁguration” on page 93 for details.)

l …/BVSNsmgr/ is the directory on the Interaction Manager and HTTP host machines where the
Interaction Manager and One-To-One HTTP gateway applications get their conﬁguration
information. The conﬁguration ﬁles in these directories must be identical for machines that run
the same One-To-One Web application. When you change an Interaction Manager
conﬁguration, you must also update the HTTP server conﬁguration. [See “Conﬁguring the
Interaction Manager server” on page 40.]

Here is a summary of some of the important ﬁles and directories that the system uses.

Files

One-To-One servers

Interaction Manager
servers

Gateway
application

$BV1TO1/*

$BV1TO1/bin/*

$BV1TO1/lib/*

System read-only ﬁles System read-only ﬁles

Executables

Libraries & default
conﬁguration ﬁles

Executables

Libraries

Orbix ﬁles

—

$BV1TO1/orbix/*

$BV1TO1/verity/* (optional)

Orbix ﬁles

Verity ﬁles

$BV1TO1_VAR/*

Site writable ﬁles

Site writable ﬁles

$BV1TO1_VAR/cache/*

$BV1TO1_VAR/collection/*
(optional)

Matching Agent

Verity collections

$BV1TO1_VAR/dbschema/*

Schema source

—

—

—

$BV1TO1_VAR/etc/*

Site conﬁguration ﬁles Site conﬁguration ﬁles

$BV1TO1_VAR/etc/.bvlog.conf

Observations

Observations

$BV1TO1_VAR/etc/bv1to1.conf

System conﬁguration Site IP addresses

(optional)

$BV1TO1_VAR/etc/bvobs.conf

Observation formats

Observation formats

—

—

—

—

—

—

—

—

—

—

—

—

—

BroadVision, Inc.

Installation and Administration Guide

Chapter 1 Introduction

3

Files

One-To-One servers

$BV1TO1_VAR/etc/roledb

—

Interaction Manager
servers

Access control roles

$BV1TO1_VAR/etc/session_terms One-To-One

—

Command Center

$BV1TO1_VAR/lib/*

Custom libraries

Custom libraries

$BV1TO1_VAR/logs/*

Observation and
system log ﬁles

Observation and system
log ﬁles

$BV1TO1_VAR/messages/*

Notiﬁcation messages —

$BV1TO1_VAR/msg_scripts/*

Notiﬁcation scripts

—

$BV1TO1_VAR/orb/*

Orbix conﬁguration

Orbix conﬁguration

Gateway
application

—

—

—

—

—

—

—

/etc/opt/BVSNsmgr/*
(UNIX only, host local)

$BV1TO1_VAR/BVSNsmgr/
(Windows NT only, host local)

…/BVSNsmgr/bvsm.ACL

…/BVSNsmgr/bvsm.cfg

…/BVSNsmgr/bvsm.req

BV1TO1_SESSION_CFG\
(Windows NT registry, host local)

/tmp/BVSNcgi_logs/
(UNIX)

BVSNSMGR_LOGS\
(Windows NT registry key)

—

—

—

—

—

—

—

—

UNIX host conﬁguration Conﬁguration

Windows NT host
conﬁguration

Conﬁguration,
when on the
Interaction
Manager host

Access control

—

Conﬁguration and HTTP
IP addresses

Interaction
Manager IP
addresses

Request cache

—

Host conﬁguration, points
to
$BV1TO1_VAR/BVSNsm
gr/

Conﬁguration

—

—

Gateway app
log ﬁles

Gateway app
log ﬁles

Database

The One-To-One database contains the information about the visitors to, and the content in your
site. What information is stored in the database is determined by the database schema, parts of
which you can conﬁgure through schema speciﬁcation ﬁles. For details about changing the schema,
see the Database Administrator’s Guide.

Additionally, much of your site’s conﬁguration information is stored in the database. This “meta
data” should never be changed directly; instead, you should modify the conﬁguration ﬁles and let
One-To-One and its utilities update the tables. However, for a complete description of the tables, see
the Database Schema Reference.

Before you start the One-To-One system, you need to have the database installed and ready to
accept One-To-One data. You identify the database and location with the environment variables
described in “Database variables” on page 33.

Installation and Administration Guide

BroadVision, Inc.

4

Chapter 1 Introduction
Configuration concepts and terminology

Configuration concepts and terminology

BroadVision uses the following terms and concepts when describing how to conﬁgure One-To-One.

application name The name of the gateway that connects to an Interaction Manager server. This is also the name that
appears in URLs that access your site. For information, see “Named applications” in “HTTP servers
and the Interaction Manager” on page 102.”

document root

The location, usually a directory, that is the root location for all HTML ﬁles. See “Directories and
URLs” in “HTTP servers and the Interaction Manager” on page 102” for details.

ﬁrewall

host

For security, your database, database accessing mechanism, and business applications usually
reside behind the security ﬁrewall. HTTP server must reside outside the ﬁrewall. The Interaction
Manager servers may reside inside or outside the ﬁrewall, and may have another ﬁrewall between it
and the One-To-One servers. [See “Firewalls” on page 106for details.]

Each machine that runs some One-To-One software — including a server, the One-To-One
Command Center, the One-To-One Design Center, and the Interaction Manager — is a host. The
One-To-One Command Center and One-To-One Design Center are Windows based applications
that run on hosts that are networked to UNIX hosts running the One-To-One and Interaction
Manager servers. After you install One-To-One, you conﬁgure it to run on that one or more hosts.
Do that by running the bvconf utility on the host where you installed One-To-One. [See “Installing
One-To-One” on page 10 for information about installing the software on the hosts.]

root directory

The directory where you install the One-To-One servers and is the value of the $BV1TO variable.
The default for a new installation is /opt/bv1to1. [See “One-To-One variables” on page 32 for more
information.]

root host

script root

site

service

Though One-To-One can be distributed among several hosts, one of the hosts manages some of the
tasks for all of the hosts. That machine is called the root host, and in addition to the things that all
hosts have in common, the root keeps track of the names and locations of all of the One-To-One
servers and objects running on your system. Deﬁne the root host by running the bvconf utility on
the machine to be the root host. [See “Installing One-To-One” on page 10 for more information.]

The directory that is the root location for all Interaction Manager scripts and page templates. See
“Directories and URLs” in “HTTP servers and the Interaction Manager” on page 102” for details.

Your organization, the one installing, running, and maintaining the One-To-One Application System
is the site. The site is responsible for managing the One-To-One system, and the applications, users,
and accounts that access the system. The site is also responsible for identifying visitors accessing the
applications within the site.

Within a site are the services that provide the content that a visitor requires. Sites are to services, what
malls are to stores, or what companies are to departments. To deﬁne a site, specify its parameters in
the One-To-One conﬁguration ﬁle. [See “Conﬁguring and starting the One-To-One servers” on page 31 for
details.]

A service provides content and utility to visitors seeking what the service provides. A service might
provide a products or information for sale to the visitor, or it might provide some other content that
speciﬁcally matches the visitor’s preferences. In the One-To-One Application System, a service
provides an application that presents the content or shopping experience to the visitor, typically
through Dynamic objects on Web pages. [See “Adding, changing or removing a service” on page 54 for
more information about conﬁguring a service.]

BroadVision, Inc.

Installation and Administration Guide

Chapter 1 Introduction
Configuration concepts and terminology

5

Installation and Administration Guide

BroadVision, Inc.

6

Chapter 1 Introduction
Configuration concepts and terminology

BroadVision, Inc.

Installation and Administration Guide

2 Installation

7

Installing and starting the One-To-One software is a three step process:

1.

Installing One-To-One as described in this chapter.

2. Preparing your system, which involves either:

• Migrating your existing system as described in Chapter 3, “Upgrading to Version 4.1,” or

• Conﬁguring and starting your new system as described in Chapter 4, “Setup.”

3. Starting your system. Both Chapter 3 and Chapter 4 describe how to start the system after you
perform the tasks in those chapters. Once your system is running, you can stop and start it per
in the instructions in “Shutting down your site” on page 138 and “Restarting your site” on
page 139.

To uninstall One-To-One, see “Removing the One-To-One Enterprise software” on page 15.

 Please be aware of the following topics before installing or upgrading your One-To-One
system:

l Installing and conﬁguring One-To-One sets up the server ﬁles that the One-To-One Command
Center and One-To-One Design Center use. For instructions about installing the One-To-One
Command Center or One-To-One Design Center, see BroadVision One-To-One Command Center
User’s Guide and One-To-One Design Center User’s Guide, respectively.

l When changing versions of One-To-One, be sure to also change the One-To-One Command

Center and One-To-One Design Center to their corresponding versions.

l The system clock on your server system must be set the same as your client machines, especially
machines running the One-To-One Command Center, so that programs that rely on date-time
will work as expected. This is especially true of incentive programs that are set to be valid for a
speciﬁc time span.

l When upgrading to a new One-To-One release, backup your database before starting the
upgrade procedure, and again after you have completed the installation and migration
activities. If you encounter any problems with the release, having these two backup states will
greatly assist you when recovering to a previously “good” state.

l The One-To-One conﬁguration ﬁles reside in the $BV1TO1_VAR/etc/ directory. These ﬁles are
not automatically updated when you change your One-To-One software release, even if you
uninstall the product per the instructions. (Leaving the ﬁles ensures that your custom changes
are not lost during the installation process.) However, if you start the system with incorrect
conﬁguration ﬁles, especially if the spoken language conﬁgurations are different, you might
encounter error messages as you try to start One-To-One. [See “Conﬁguring the One-To-One
environment and services” on page 37 for information.]

Installation and Administration Guide

BroadVision, Inc.

8

Chapter 2 Installation
Prerequisites

l To avoid corrupting the One-To-One databases, make sure that the server machines are on
uninterruptable power supplies (UPSs) that will keep the machines running for at least one
minute in the event of a power failure.

l To run different versions of One-To-One on the same host, follow the instructions in “Running

multiple One-To-One servers on one host” on page 92.

Prerequisites

Before installing One-To-One:

l Check the One-To-One Server Release Notes for the latest and most accurate system and software

requirements. The values in the Release Notes supersede any in this manual.

l The Rogue Wave development libraries (for development systems)

l The Verity search engine requires an additional license for use; it is not part of the standard

BroadVision One-To-One Enterprise license. If you plan to install the Verity software, you must
ﬁrst obtain a Verity run-time license from BroadVision.

l The machine that will host One-To-One must be registered with your network’s Domain Name
Server (DNS). Even if the machine is running stand-alone — isolated from a network — it must
have a DNS entry.

If you suspect a DNS conﬁguration problem, try looking up the IP address of the host with
nslookup. Also try reverse DNS lookup. For example, if a One-To-One Command Center
running on Windows NT fails to connect to a host name “hercules” (IP address 255.255.166.66),
run the following commands on both the server and client machines. If DNS is not properly
conﬁgured, one will report “Non-existent domain” error.

nslookup hercules
nslookup 255.255.166.66
nslookup -q=any 66.166.255.255.in-addr.arpa

l The One-To-One conﬁguration ﬁles reside in the $BV1TO1_VAR/etc/ directory. These ﬁles are
not automatically updated when you change your One-To-One software release, even if you
uninstall the product per the instructions. (Leaving the ﬁles ensures that your custom changes
are not lost during the installation process.) However, if you start the system with incorrect
conﬁguration ﬁles, especially if the spoken language conﬁgurations are different, you might
encounter errors as you try to start One-To-One.

BroadVision, Inc.

Installation and Administration Guide

Chapter 2 Installation
Prerequisites

9

l Your database management system (DBMS) must already be installed. The account that will be
running One-To-One will need “create object” access rights [see “Database variables” on page 33
for more information about the access rights]. Allocate at least 35MB for the body of the database,
and at least 5MB for database transaction logging; see the One-To-One Server Release Notes for
actual requirements. To free space, be sure to purge the transaction logs when you back up the
system. If you do not have enough free space, the database management system might hang.

Oracle systems

• Create an alias for accessing the database. The name you assign to this alias will be used by
One-To-One to access the database. This is the value you will assign to the BV_DB_SERVER
and BV_DB_DATABASE environment variables.

• Windows NT hosts: Install either the Oracle client utilities or the Oracle server package. You
must choose Administrator access in either case; otherwise the installation process will not
install all of the necessary ﬁles.

• Windows NT hosts: To access an Oracle DBMS installed on a UNIX system, you must install
the client utilities on the Windows NT host. The account that will access the One-To-One
database must be granted these privileges:

CONNECT
DBA
EXP_FULL_DATABASE
IMP_FULL_DATABASE
RESOURCE
SNMPAGENT

SQL Server systems

• For SQL Server database systems, if you intend to use observation logging and loading, the
database user performing the loading must be the database owner (DBO). Only the DBO
has the privileges necessary to complete the loading process, especially adding and
dropping tables and stored procedures. The DBO status can be reassigned to a different
user; however, only one DBO can exist per database. Only one login ID can be the DBO
login ID, although other login IDs can be aliased to the DBO.

• In western European locales, when you conﬁgure SQL Server, turn off Automatic ANSI to

OEM conversion, because ISO 8859-1 (referred to as ANSI) is the default SQL Server
character set encoding Windows and Windows NT. To turn off the Automatic ANSI to OEM
conversion, use the SQL Server client utility(\MSSQL\BINN\WINDBVER.EXE)."

• In German locales, turn off the Automatic ANSI to OEM conversion checkbox in the SQL

Server client utility (\MSSQL\BINN\WINDBVER.EXE).

• If you are accessing MSSQL over a local area network, the MSSQL 7.0 client must be

installed before you install One-To-One.

l To ensure the security of the information in the One-To-One databases, make sure that the

One-To-One system ﬁles and databases are on machines behind a ﬁre wall; locate the visitor
accessible machines outside of the ﬁre wall. [See “Firewalls” on page 106for details.]

l To avoid corrupting the One-To-One databases, make sure that the server machines are on
uninterruptable power supplies (UPSs) that will keep the machines running for at least one
minute in the event of a power failure.

l If you are going to use any of the following support packages, they must be installed before

One-To-One tries to access them:

• The AVP tax package [see “Installing AVP Taxware” on page 124 for more information].

• The Verifone Omnihost Payment Handler (Solaris only) [see “Conﬁguring Omnihost (Solaris

only)” on page 135 for more information].

Installation and Administration Guide

BroadVision, Inc.

10

Chapter 2 Installation
Installing One-To-One

Installing One-To-One

If you are installing for the ﬁrst time, follow the instructions in this section. If you are upgrading
from an earlier version of One-To-One, review “Running multiple One-To-One servers on one host”
on page 92 for information about things to consider about simultaneously running both an old and
new version of One-To-One.

CAUTION Never:

• Install one version of One-To-One on top of an existing version. Always uninstall the old

version ﬁrst, or install the new version in a new location.

• Allow an older version of One-To-One to access a database that has been used by a newer

version.

Before installing One-To-One, review the “Prerequisites” described in the previous section of this
manual, and check the Server Release Notes for any other important last-minute instructions,
problems, or considerations.

The rest of this section describes how to install One-To-One on

l Solaris, which is described next, and on

l HP-UX, which described in “Installing One-To-One on HP-UX” on page 12.

l Windows NT, which described in “Installing One-To-One on Windows NT” on page 14.

When you are ﬁnished installing One-To-One, if you are

l Upgrading from an older version of One-To-One, follow the instructions in Chapter 3,

“Upgrading to Version 4.1,” before starting the new installation.

l Installing One-To-One for the ﬁrst time, follow the instructions in Chapter 4, “Setup.”

Installing One-To-One on Solaris

BroadVision delivers the One-To-One software on a CD-ROM. You must install the software on the
root host, the machine that manages the One-To-One servers.

To install One-To-One,

1. Become super-user in csh:

% su

2. Make sure that the location where you are going to install One-To-One has the minimum free
disk space required per the System and software requirements speciﬁcation in the One-To-One
Server Release Notes.

3. Make sure that you have /usr/sbin in your path. The sbin directory contains Solaris package

utilities that install uses.

# PATH=$PATH:/usr/sbin
# export PATH

4. Mount the CD-ROM in the usual way. On Solaris, you usually mount the CD-ROM by inserting

it in the drive.

BroadVision, Inc.

Installation and Administration Guide

Chapter 2 Installation
Installing One-To-One

11

5. Change to the solaris directory. The following example assumes that your CD-ROM drive is

drive #0:

# cd /cdrom/cdrom0/solaris

6. Run the install script. The script prompts for information about your environment.

# ./install

If you are not a super-user, a prompt asks if you want to install or rehearse the installation; you
must be super-user to complete the installation. Enter “N” to terminate the installation so you
can log in as super-user [see Step 1], or enter “Y” to rehearse the installation. A rehearsal allows
you to see what install will do, without actually installing the product.

7. Specify the installation package’s source device or directory. You should be able to choose the

default value provided. Give the full-path to the directory that contains this script and
packages, such as: /cdrom/bv1to1/solaris

8. For standard licenses, conﬁrm that you want a default installation by choosing “y”.

• If you have a license for the Verity search software, choose “n”.

Choose “y” for all of the remaining prompts, especially the one to conﬁrm installation of the
Verity software.

• Otherwise, you should never have to use a non-default installation.

9. Specify the language of your locale. The default should be correct for your locale.

10. Specify which database management system you are using: “Oracle”, “Sybase”, or “Informix”.

11. Specify the directory where you want to install One-To-One. Either specify a new directory, or

press Return to install One-To-One in the default, which for a new installation is
/opt/bv1to1. This directory is referred to as the One-To-One root directory, or $BV1TO1.

The install process then displays the information about the installation to perform.

12. Conﬁrm that you want to perform the installation.

The install process then displays the information similar to the following as it progresses:

Installing the following packages:
BVBase BVBaseS BVSvc BVSvcS

pkgadd -a /usr/tmp/admin-22428 \

-d "/cdrom/Solaris/pkg.Solaris" BVBase BVBaseS BVSvc

If you receive error messages about insufficient disk space, remove the partially installed
package by following the instructions in “Removing the One-To-One Enterprise software” on
page 15. Free some disk space, and then re-install One-To-One per the instructions in this
section.

When install ﬁnishes, it displays “Done.”

13. Log out of super-user access.

This concludes the installation process. You can now repeat these steps for each machine that will
run One-To-One, or move on to upgrading or conﬁguring the system:

l If you are installing One-To-One for the ﬁrst time, go to Chapter 4, “Setup.”

Installation and Administration Guide

BroadVision, Inc.

12

Chapter 2 Installation
Installing One-To-One

l If you are upgrading from an earlier version of One-To-One, follow the upgrade instructions in
Chapter 3, “Upgrading to Version 4.1.” Do not start the One-To-One system until you have
completed the steps described in that chapter.

l If you intend to install the One-To-One Enterprise Broadway sample application, you must
install it [see “Conﬁguring the Broadway sample application” on page 50] before installing any
BroadVision One-To-One applications, such as One-To-One Publishing Center

Installing One-To-One on HP-UX

BroadVision delivers the One-To-One software on a CD-ROM. You must install the software on the
root host, the machine that manages the One-To-One servers.

Installing One-To-One directly from the CD-ROM takes 1.5 to 2.0 hours. BroadVision recommends
that you copy the installation ﬁles to a local disk and then run the INSTALL script from the local disk.
Running the INSTALL script from a local disk takes only 15 to 20 minutes, including the time
needed for copying the installation ﬁles.

To install One-To-One,

1. Become super-user in csh:

% su

2. Make sure that you have free disc space enough to contain the installed One-To-One product,

and a copy of the CD-ROM source ﬁles. See the One-To-One Server Release Notes for information
about space requirements.

3. Mount the CD-ROM by putting the disc in the CD-ROM drive and running mount:

# mount /cdrom

If the drive does not mount, make sure that the /etc/fstab ﬁle contains an entry for the drive.
The ﬁle should contain an entry similar to this:

/dev/dsk/c1t2d0 /cdrom cdfs ro,suid,noauto 0 0

4. Create a temporary storage directory on a drive that has at least 385 MB of space available, and

copy the platform installation ﬁles to the temporary directory. For example,

# mkdir /var/tmp/v4.1
# cp /cdrom/HPUX /var/tmp/v4.1

5. Change to the temporary directory and perform the installation from there.

# cd /var/tmp/v4.1

6. Run the INSTALL script. The script prompts for information about your environment.

# ./INSTALL

BroadVision, Inc.

Installation and Administration Guide

Chapter 2 Installation
Installing One-To-One

13

7. Specify the directory where you want to install One-To-One. Either specify a new directory, or
press Return to install One-To-One in the default, which for a new installation is /opt/bv1to1.
This directory is referred to as the One-To-One root directory, or $BV1TO1.

On HP-UX, the prompt displays the root directory (/). This is the location where INSTALL puts
the opt/bv1to1 directory. If you want to specify another directory, type “other” and then at
the next prompt, enter the path of the directory that should contain the opt/bv1to1 directory.
For example, if you enter other and then specify /etc, INSTALL creates /etc/opt/bv1to1.

If you choose other to install in a non-default directory, you must create a directory named
/etc/opt/BVSNsmgr and give it group and world read/write access.

8. If you are not a super-user, a prompt asks if you want to install or rehearse the installation; you
must be super-user to complete the installation. Enter “N” to terminate the installation so you
can log in as super-user (see Step 1), or enter “Y” to rehearse the installation. A rehearsal allows
you to see what INSTALL will do, without actually installing the product.

9. Specify the installation package’s source device or directory. You should be able to choose the

default value provided. Give the full-path to the directory that contains this script and
packages, such as: /cdrom/HPUX/

10. Conﬁrm that you want a default installation by choosing “y”. You should never have to use a

non-default installation.

11. Specify the language of your locale. The default should be correct for your locale.

For this release, you must specify U.S. English or Japanese.

12. Specify which database management system you are using: “Oracle”, “Sybase”, or “Informix”.

The install process then displays the information about the installation to perform.

13. Conﬁrm that you want to perform the installation.

The install process then displays the information similar to the following as it progresses:

Installing BroadVision products
BVBase BVBaseS BVSvc BVSvcS

swinstall -s /cdrom/BV1TO1/HPUX/bvsn_thirdparty BVSNbsb @ /opt/bv1to1

...

The following error conditions might occur:

• If you receive error messages about insufﬁcient disk space, remove the partially installed

package by following the instructions in “Removing the One-To-One Enterprise software”
on page 15. Free some disk space, and then re-install One-To-One per the instructions in this
section.

• During installation, erroneous messages appear for each swinstall command that install
executes. These messages, “1 postinstall or postremove script had warnings” and “Cannot
open the logﬁle on this target or source,” can be ignored.

When INSTALL ﬁnishes, it displays “Done.”

14. Remove the temporary storage directory and the installation ﬁles it contains.

# rm -rf /var/tmp/v4.1

15. Log out of super-user access.

Installation and Administration Guide

BroadVision, Inc.

14

Chapter 2 Installation
Installing One-To-One

This concludes the installation process. You can now repeat these steps for each machine that will
run One-To-One, or move on to upgrading or conﬁguring the system:

l If you are installing One-To-One for the ﬁrst time, go to Chapter 4, “Setup.”

l If you are upgrading from an earlier version of One-To-One, follow the upgrade instructions in
Chapter 3, “Upgrading to Version 4.1.” Do not start the One-To-One system until you have
completed the steps described in that chapter.

l If you intend to install the One-To-One Enterprise Broadway sample application, you must
install it [see “Conﬁguring the Broadway sample application” on page 50] before installing any
BroadVision One-To-One applications, such as One-To-One Publishing Center

Installing One-To-One on Windows NT

To install One-To-One:

1. Log in with an “administrator” account. The account that you use to install and run One-To-One
must have “administrator” privileges, and must have the right to “Log on as a Service”. This
right is granted with the Windows NT User Manager tool. This is the account that the
One-To-One servers will use. [See “Starting the One-To-One servers” on page 38 for more
information.]

2.

Install the MKS Toolkit. MKS is provided on the One-To-One CD. To install it, run the MKS Setup
program:

\windows\mks\x86\setup.exe

a. When installing MKS, a prompt will ask you for the product serial number, enter:

4412451631

b. When setup prompts for the destination in which to install MKS, choose a directory whose

path is comprised of valid DOS ﬁlenames (8.3 format: 8 character maximum name, 3
character maximum extension). For example, do not install MKS in the Windows/NT
“Program Files” directory (c:\winnt\Program Files\mks) because it is not a valid
DOS path. A good place to install MKS is off the root directory in c:\mks.

BroadVision, Inc.

Installation and Administration Guide

Chapter 2 Installation
Removing the One-To-One Enterprise software

15

c. Choose the Typical installation when prompted; select Microsoft 32 bit compiler.

3. Restart Windows NT before continuing.

4. Define the One-To-One root directory (the directory where One-To-One is installed). Choose a

directory whose path is comprised of valid DOS ﬁlenames (8.3 format: 8 character maximum
name, 3 character maximum extension, no spaces). For purposes of instructions, the rest of the
examples in this document assume that you have installed One-To-One in D:\bv1to1. This is
known as the One-To-One root directory or $BV1TO1.

5.

Install One-To-One. Run the Setup program from the Windows\Servers directory on the CD.

\windows\servers\setup.exe

It will tell you that it is going to install One-To-One and Orbix. Optionally, if you have a license
for the Verity search software, you may choose to install that component. You must have a
license to install and use this option.

Removing the One-To-One Enterprise software

These instructions describe how to remove the BroadVision One-To-One Enterprise software.

Removing a Windows NT installation

To uninstall the One-To-One system:

1. Shut down the system as described in “Shutting down your site” on page 138.

2. Back up the system as described in “Backing up your site” on page 141.

3. Restart Windows NT.

4. Remove the orbixd service entry by running:

$BV1TO1/orbix/bin/orbixds -u

5. Use Uninstall Shield from the Add-Remove Program Control Panel to uninstall One-To-One.

6. Restart Windows NT.

Removing a UNIX installation

The CD-ROM that contains the One-To-One software contains a “uninstall” script that knows how
to remove the software. This script does not remove your site-speciﬁc data in the $BV1TO1_VAR
directory.

To remove the One-To-One servers from your UNIX system:

1. Shut down the system as descried in “Shutting down your site” on page 138.

2. Back up the system as described in “Backing up your site” on page 141.

3. Mount the CD-ROM that contains the One-To-One software from BroadVision.

Installation and Administration Guide

BroadVision, Inc.

16

Chapter 2 Installation
Removing the One-To-One Enterprise software

4. Change to the platform directory on the CD-ROM.

On Solaris, change to the solaris directory. The following example assumes that your
CD-ROM drive is drive #0:

% cd /cdrom/cdrom0/solaris

On HP-UX, change to the HPUX directory.

% cd /cdrom/HPUX

5. Become super-user.

% su

6. Remove the One-To-One software by running the uninstall script:

On Solaris, run uninstall:

% uninstall

The uninstall process on Solaris removes all One-To-One system files on the host, including
those from previous versions.

On HP-UX, run UNINSTAL:

% UNINSTAL

During the uninstall, you might get a warning about package dependency failures. You can
ignore this warning and press “Y” to continue the uninstall.

BroadVision, Inc.

Installation and Administration Guide

3 Upgrading to Version 4.1

17

If you are upgrading your One-To-One site from a older version, follow the instructions in this
chapter to conﬁgure and start your Version 4.1 system. However, if you have just installed Version
4.1 and have never installed One-To-One on your system, skip to the instructions in Chapter 4,
“Setup.”

These instructions describe how to upgrade from Version 3.0 and Version 4.0. If your existing
system is older, contact BroadVision for assistance.

CAUTION Do not start the Version 4.1 servers or change the bv1to1.conf conﬁguration file until

after you have performed the migration process.

The basic steps for upgrading your system to Version 4.1 are:

1. Prepare the system for migration as described in “Migration prerequisites,” next.

2. Copy the conﬁguration ﬁles and directories, as described in “Replicating directories and

conﬁguration ﬁles” on page 20.

3. Upgrade the database schema as described in “Migrating the database schema” on page 21.

4. Update the system conﬁguration ﬁles as described in “Migrating system conﬁguration” on

page 23.

5. If you are upgrading from Version 4.0, ﬁx the scripts that use BVI_Visitor.visitor()

retrieve visitor information by ID, as described in “Updating Version 4.0 scripts” on page 27.

6. Rebuild any custom components and Dynamic Objects as described in “Updating components

and dynamic objects” on page 28.

7. Update the client One-To-One Command Center, and One-To-One Design Center installations

to use the ones supplied with this version.

You can then start One-To-One Version 4.1 per the instructions in “Starting the One-To-One servers”
on page 38 and “Starting the Interaction Manager” on page 42.

See “Running multiple One-To-One servers on one host” on page 92 for information about
running old and new versions of One-To-One at the same time.

Installation and Administration Guide

BroadVision, Inc.

18

Chapter 3 Upgrading to Version 4.1

Overview

When upgrading a One-To-One site, you need to install the new software while preserving your
existing site’s conﬁguration and data. The safest way to accomplish this is to install the new
software on host machines or ﬁle locations different from the existing system, and then migrate the
conﬁguration and data to the new system. These instructions describe that scenario as it pertains to
a multi-host conﬁguration: one where the One-To-One, Interaction Manager, and HTTP servers
reside on separate hosts that do not, necessarily, have access to the same ﬁle systems [See “Running a
multiple-host conﬁguration” on page 93 for more information].

One-To-One and Interaction Manager server conﬁguration information resides in the
$BV1TO1_VAR directory hierarchy. That directory structure must be moved to the new system. The
Interaction Manager and HTTP gateway application get additional conﬁguration information from
the bvsm.cfg ﬁle. You may copy this to the new Interaction Manager host, but you must update the
conﬁguration before starting the servers. The HTTP server’s document root, and the Interaction
Manager’s script root and start-up scripts directories must be copied to the new system. The
database content should be moved to a new database, per the instructions in your DBMS’s
documentation.

After installing the new One-To-One software, be sure that the gateway application is the one
provided with the new system. Update all pertinent environment variables, and recompile all
custom libraries before starting the system.

Old system

New system

HTTP server

/doc-root/
bvsm.cfg
gateway app

Copy directory

New

HTTP server

/doc-root/
bvsm.cfg
gateway app

Interaction Manager

Interaction Manager

/script-root/
/startup-scripts/
bvsm.cfg
$BV1TO1/
$BV1TO1_VAR/
…/lib/*

Copy directory
Copy directory
Optional copy then update

Recompile libs

/script-root/
/startup-scripts/
bvsm.cfg
$BV1TO1
$BV1TO1_VAR/
…/lib/*

One-To-One servers

$BV1TO1_VAR/
$BV1TO1/

Copy directory

Change system variables

One-To-One servers

$BV1TO1_VAR/
$BV1TO1/

Copy

Can be the same
or exactcopies of
the directories on
the One-To-One
servers host

One-To-One
database

Replicate database, and
change system variables

One-To-One
database

The rest of this chapter describes these upgrade steps in detail.

BroadVision, Inc.

Installation and Administration Guide

Migration prerequisites

Before you begin the migration process, you need to:

Chapter 3 Upgrading to Version 4.1
Migration prerequisites

19

1. If you haven’t done so already, shut down the old BroadVision One-To-One Enterprise system

per the instructions in “Shutting down your site” on page 138. To summarize:

a. Use imgr_conf to shut down all running Interaction Managers on each machine that hosts
an Interaction Manager. If you have multiple Interaction Managers running on a host, be
sure to specify the installation name of each. [See “Named applications” on page 104 for more
information.]

. $BV1TO1_VAR/etc/bv1to1.conf.sh
$BV1TO1/bin/imgr_conf -a stop

b. Shut down all active One-To-One Command Center sessions, and any applications that are

clients of One-To-One.

c. Shut down the connections from the existing business system (back end).

d. From the root host, use bvconf to shut down the site.

bvconf shutdown

If the shut down reports any errors, manually kill the offending processes with kill.

e. Wait for the servers to ﬁnish shutting down before accessing or changing the system.

2. Backup your database.

3. Backup the $BV1TO1_VAR/etc and $BV1TO1_VAR/dbschema directories. These include your

site’s system conﬁguration and database schema information.

If for whatever reason the migration stops before it completes:

a. Remove all ﬁles from these directories.

b. Repopulate the directories from the backup.

c. Reload the database from its backup.

d. Restart the migration process.

4. On Windows NT systems, uninstall One-To-One Version 3.0:

a. Restart Windows NT.

b. Remove the orbixd service entry by running:

%BV1TO1%\orbix\bin\orbixds -u

c. Use Uninstall Shield from the Add-Remove Program Control Panel to uninstall

One-To-One.

d. Manually delete all of the registry entries under these

HKEY_LOCAL_MACHINE\SOFTWARE\ entries:

...\Broadvision\One-To-One Application System\3.0
...\IONA Technologies\Orbix\2.2

Installation and Administration Guide

BroadVision, Inc.

20

Chapter 3 Upgrading to Version 4.1
Replicating directories and configuration files

e. If you are removing the One-To-One system Version 3.0 for German locales, remove the

BroadVision report manager. Use the setup.exe program located in the
Report Manager\setup\ directory to remove the manager.

f. From the System Control Panel, edit the PATH environment setting and remove the

D:\bv1to1\bin and D:\bv1to1\orbix\bin settings.

g. Restart Windows NT.

5. Install but do not start Version 4.1. Follow the instructions in “Installing One-To-One” on

page 10. You might also want to read “Running multiple One-To-One servers on one host” on
page 92.

6. Windows NT: Shut down any virus checking software. Many virus checkers, especially McAfee
VirusScan, report erroneous messages when starting the One-To-One and Interaction Manager
servers.

CAUTION Never allow:

l an older version of One-To-One to access a database that is being used for a newer version.

l two installations of One-To-One to access the same $BV1TO1_VAR directory at the same time.

Also, two installations of One-To-One should avoid accessing the same database at the same time.
See “Running a multiple-site conﬁguration” on page 95 for details about how to do it safely.

Replicating directories and configuration files

The instructions in this section assume that you are installing the new version in locations different
from the old version. See “Overview” on page 18 if you are not sure which conﬁguration you have.

1. For the root host — the machine where you run bvconf to start the One-To-One servers — copy

the old $BV1TO1_VAR directory tree to the new location.

2. For each Interaction Manager host:

a. Copy the old script root directory tree to the new location. This directory contains the scripts
that make up your site’s application. If you have page templates, they should be in this
directory tree too.

b. Copy the old start-up scripts directory to the new location. These are the scripts that the

Interaction Manager runs when it starts.

c. Copy the bvsm.cfg — or appname.cfg — ﬁle(s) to the new location. They must be in the

same directory location on the new host as they were in the old host. See “Named
applications” on page 104 if you are not sure which ﬁle or where they are located.

3. For each HTTP host, copy the document root ﬁles or directories used by your One-To-One

application from the old to the new location.

You can now migrate the database.

BroadVision, Inc.

Installation and Administration Guide

Migrating the database schema

Chapter 3 Upgrading to Version 4.1
Migrating the database schema

21

To migrate the database, you will run scripts provided in the new release that read the old schema,
and update the new schema to contain your custom schema changes. Before running the scripts,
you will need to setup the environment with most of the environment settings that were used by
your old system.

To migrate your existing BroadVision One-To-One Enterprise database to Version 4.1:

1. If you are replicating the old database to a new one, do that now per the instructions in your

DBMS’ documentation. In Step 4 below, be sure to update your $BV_DB_SERVER,
$BV_DB_DATABASE, and $BV_DB_USER environment variables.

• If you are updating versions on your DBMS, follow the DBMS’ instructions for migrating the
database data to the new version. Not all DBMS updates require data migration, though
some require you to dump the old tables and load into the new.

2. Set the system environment variables to match your existing One-To-One system. The variables
are deﬁned in a shell script in the Version 4.1 $BV1TO1_VAR/etc directory (you put them there
per the instructions in “Replicating directories and conﬁguration ﬁles” on page 20. However,
you need to modify the shell scripts before you source them:

a. Locate the shell script in $BV1TO1_VAR/etc and edit the one appropriate for your

environment.

csh:

bv1to1.conf.csh

sh, ksh, or MKS:

bv1to1.conf.sh

b. In the shell ﬁle, remove or comment-out these setting:

csh:

setenv PATH ...

sh, ksh, or MKS:

export PATH...

HP-UX:

Solaris:

export SHLIB_PATH ...

export LD_LIBRARY_PATH...

c. Save the edited ﬁle.

d. Create a new terminal shell, such as with xterm or MKS, to ensure that the environment

settings are fresh.

e. Set the One-To-One variables in your shell:

csh:

% source $BV1TO1_VAR/etc/bv1to1.conf.csh

sh, ksh, or MKS:

$ . $BV1TO1_VAR/etc/bv1to1.conf.sh

3. Set $BV1TO1 to the root directory of the Version 4.1 installation.

Installation and Administration Guide

BroadVision, Inc.

22

Chapter 3 Upgrading to Version 4.1
Migrating the database schema

4. Check that your $BV1TO1_VAR, $BV_DB_SERVER, $BV_DB_DATABASE, and $BV_DB_USER
environment variables are set to the Version 4.1 settings. [See “Deﬁning system environment
variables” on page 31 for details.]

• If you changed the database in Step 1 above, update the database settings as well. [See

“Database variables” on page 33 for details.]

5. Set $PATH to pick up the executables and libraries from the Version 4.1 installation.

csh:

setenv PATH $BV1TO1/bin:$BV1TO1/orbix/bin:$PATH

sh or ksh:

export PATH; PATH=$BV1TO1/bin:$BV1TO1/orbix/bin:$PATH

MKS:

export PATH; PATH=$BV1TO1/bin:$BV1TO1/orbix/bin:$PATH

6. On UNIX, set $LD_LIBRARY_PATH (Solaris) or $SHLIB_PATH (HP-UX) to pick up the

executables and libraries from the Version 4.1 installation. The value of these settings cannot
contain white space or be broken. The following examples are broken to ﬁt this documentation.

Oracle systems — include the $ORACLE_HOME/lib directory, like this:

setenv LD_LIBRARY_PATH $BV1TO1/lib:$ORACLE_HOME/lib
:$BV1TO1/rogue/lib:$BV1TO1/orbix/lib:$LD_LIBRARY_PATH

Informix systems — include the $INFORMIXDIR/lib/esql and $INFORMIXDIR/lib
directories, like this:

setenv LD_LIBRARY_PATH $BV1TO1/lib:$INFORMIXDIR/lib
:$INFORMIXDIR/lib/esql:$BV1TO1/rogue/lib:$BV1TO1/orbix/lib
:$LD_LIBRARY_PATH

7. Set the $BV_LC_LIST environment variable to correct value for your locale:

Solaris:

HP-UX:

setenv BV_LC_LIST en_US

setenv BV_LC_LIST en_US.iso88591

Windows NT:

export BV_LC_LIST; BV_LC_LIST=usa

8. Migrate the schema by running the migrate_to_v4.1 script:

cd $BV1TO1/bin/scripts/loader/
./migrate_to_v4.1 $BV_DB_SERVER $BV_DB_DATABASE $BV_DB_USER password

This utility prompts for additional information:

• Answer ‘Y’ when it asks for permission to modify the $BV1TO1_VAR/dbschema and

$BV1TO1_VAR/dbschema/tmp directories (if it does ask).

If the directory is incorrect, answer “n” to terminate the script. Then, adjust the
$BV1TO1_VAR setting to point to the correct location and restart the script. Note that you do
not have to restore from backups or repopulate the database at this time.

• When it displays the name of the log ﬁle, make a note of the name, you might need it later.

• Conﬁrm that you want to proceed with the migration to 4.1 by answering ‘Y’.

BroadVision, Inc.

Installation and Administration Guide

Chapter 3 Upgrading to Version 4.1
Migrating system configuration

23

If the migration fails, review the error messages displayed and examine the log ﬁle to determine
the cause of the error. Also review the $BV1TO1_VAR/logs/hostName/bvlog*.out log ﬁle
and look for errors.

Note that you can ignore errors similar to these if you ﬁnd them:

"cannot create a table because the table already exists."
"cannot drop a table because the table does not exist."
"bv1to1.conf.o not being found in bvlog."

If any other error occurs during the migration and the migration stops before completing,
resolve the problem identiﬁed in the log ﬁle, and then

a. Remove all ﬁles from the $BV1TO1_VAR/dbschema and $BV1TO1_VAR/etc directories.

b. Repopulate the directories from the backup.

c. Reload the database from its backup.

d. Restart the migration process.

You have completed the migration of the database. Next you need to migrate your system
conﬁguration.

Migrating system configuration

To migrate your system conﬁguration, you need to update the bv1to1.conf, .bvlog.conf, and
bvsm.cfg (or appName.cfg) conﬁguration ﬁles. To update and install the conﬁguration updates
into your One-To-One system, determine your existing conﬁguration settings and apply them to the
new conﬁguration ﬁles.

Server
conﬁguration

The default Version 4.1 bv1to1.conf has new deﬁnitions and comments. As such, it is not
practical to perform a ﬁle comparison between your existing ﬁle and the new one to determine what
is different. Instead, ﬁrst perform a comparison between your existing conﬁguration ﬁle and the
default ﬁle that shipped with the older version, and then make the changes to the Version 4.1 ﬁle. To
do that:

1. Locate the default conﬁguration ﬁle that came with your older One-To-One software. It is the

<old-$BV1TO1>/lib/bv1to1.conf.default.

2. Locate your custom ﬁle from the older version. It is

<old-$BV1TO1_VAR>/etc/bv1to1.conf.

3. Compare the two ﬁles and note the changes. One way to do this is with the UNIX or MKS diff

utility.

4. Copy the Version 4.1 default ﬁle to your Version 4.1 $BV1TO1_VAR/etc/ directory. Rename the

ﬁle, and make it writable.

cp $BV1TO1/lib/bv1to1.conf.default $BV1TO1_VAR/etc/bv1to1.conf
chmod +w $BV1TO1_VAR/etc/bv1to1.conf

Installation and Administration Guide

BroadVision, Inc.

24

Chapter 3 Upgrading to Version 4.1
Migrating system configuration

5. Edit the new ﬁle Version 4.1 ﬁle ($BV1TO1_VAR/etc/bv1to1.conf) and update the

parameters that you customized in your older One-To-One ﬁle.

a. In Version 3.0, the Payment system used processes. Beginning with Version 4.1, the system
uses daemons. Change these Payment Handling system deﬁnitions from “process” to
“daemon [see the bv1to1.conf ﬁle for examples]: pmtassign_d, pmtsettle_d, and
pmthdlr_d

Here is a partial list of the parameters new or changed in this release:

adm_srv (process)

Obsolete, not used, and removed in 4.1.

BV1TO1_INSTANCE (Windows NT only)

Server instance name.

BV_ORB_BIDIRECTIONAL_IIOP

Future for Orbix 2.3, not used in 4.1.

bv_schedule_dynamic_msgcount

Changed, default count reduced to 500

bv_schedule_static_msgcount

Changed, default count reduced to 500

BVLOG_DIR

CommandCenter (group)

Log directory.

New, reserved name, identiﬁes processes to be used by the
Command Center only.

DBCENTURY (Informix only)

gdb_query_cache_size

New for Informix, Year 2000 handler.

New, generic database accessor query cache size

gdb_query_cache_timeout

New, generic database accessor query cache time-out limit.

gdb_query_limit

IT_MAX_MESSAGE_SIZE

query_cache_timeout

New, generic database accessor return count limit.

Future for Orbix 2.3, not used in 4.1.

New, query cache time-out limit.

smgr_first_port_minimum

New, used by imgr_conf when scanning for available ports.

For information about the parameters, see “bv1to1.conf” on page 161.

Logging
conﬁguration

The .bvlog.conf has been updated to include new logging conﬁgurations. To install your
customizations into the ﬁle:

1. Compare your existing .bvlog.conf ﬁle with the default Version 4.1 ﬁle, and update the ﬁle

to include the new parameters.

$BV1TO1_VAR/etc/.bvlog.conf
$BV1TO1/lib/bvlog.conf.default

Old file
New default file

For information about this ﬁle, see “.bvlog.conf” on page 184.

BroadVision, Inc.

Installation and Administration Guide

Apply the
changes

After updating the conﬁguration ﬁles:

1. Start the One-To-One servers with the bvconf command’s execute option. This will read the

new conﬁguration settings.

$BV1TO1/bin/bvconf execute

Chapter 3 Upgrading to Version 4.1
Migrating system configuration

25

You might see an error about not being able to access “bv1to1.conf.o”. You can ignore this
message at this time.

bvconf execute
One-To-One on earth: Check installation
One-To-One on earth: System pre-check is done.
mv: cannot access .../store_mig/etc/bv1to1.conf.o
One-To-One on earth: System pre-check is done.

2. If your Version 3.0 site has matching rules that return categories, rather than content, update the
rule sets with the migr_coll utility. [See “migr_coll” on page 197 for details.] You can skip this
step if you are migrating from Version 4.0.

$BV1TO1/bin/migr_coll

3. After successfully starting the system, stop the servers with the bvconf command’s shutdown

option:

$BV1TO1/bin/bvconf shutdown

4. Start a new terminal shell, such as xterm or MKS, and continue with the remainder of the

migration instructions by executing commands in the new shell. This will ensure that you do
not have erroneous environment settings left over from earlier activities.

5. Set the One-To-One variables in your new shell’s environment:

csh:

% source $BV1TO1_VAR/etc/bv1to1.conf.csh

sh, ksh, or MKS:

$ . $BV1TO1_VAR/etc/bv1to1.conf.sh

Installation and Administration Guide

BroadVision, Inc.

26

Chapter 3 Upgrading to Version 4.1
Migrating system configuration

Interaction
Manager
conﬁguration

You can now update the Interaction Manager conﬁguration. Before you proceed, you should read
“HTTP servers and the Interaction Manager” on page 102 for an overview about how the Version
4.1 Interaction Manager communicates with the HTTP server.

1. Update the Interaction Manager conﬁguration to include the new settings.The Version 4.1

editor reads your older version settings and presents them as default values for the prompts.

$BV1TO1/bin/imgr_conf -a configure

You must run imgr_conf -a configure at least once to update the conﬁguration ﬁle to the
current conﬁguration settings. The interactive editor displays message and prompts for
Interaction Manager settings. This process now includes highly descriptive prompts. If you are
not sure about how to answer one, consult Chapter 6, “Interaction Manager conﬁguration.

• At the “Enter the path to where your component and dynamic object libraries are installed”

prompt, change the object library directory to the new Version 4.1 location, such as:

UNIX

Windows NT

/opt/bv1to1_4.1/lib/components:
/opt/bv1to1_4.1_var/lib/objects:
/host/a/lib/components:/host/a/lib/objects

D:/bv1to1_4.1/lib/components;
D:/bv1to1_4.1_var/lib/objects;
F:/a/lib/components;F:/a/lib/objects

Note that the lines above was broken to ﬁt this documentation; it must be entered as one string.

• At the “What is the full path to the directories where your start up scripts are installed”
prompt, change the path to the location of your Version 4.1 installation’s start-up script
directories, such as:

UNIX

Windows NT

/opt/bv1to1_4.1/script_library:
/opt/bv1to1_4.1_var/lib/script_library

D:/bv1to1_4.1/script_library:
D:/bv1to1_4.1_var/lib/script_library

Note that the line above was broken to ﬁt this documentation; it must be entered as one string.

2. Repeat the previous step on all Interaction Manager hosts.

3. Update your HTTP server to use the Version 4.1 gateway program:

For standard CGI default installations, copy inetcgi or inetcgi.exe into your HTTP
“executables” directory [see “Conﬁguring the gateway for a standard CGI server” on page 48 for more
information]:

UNIX

cp $BV1TO1/bin/inetcgi /home/http/cgi-bin/inetcgi

Windows NT cp $BV1TO1/bin/inetcgi.exe D:/InetPub/cgi-bin/inetcgi.exe

For standard CGI named installations (see “Named applications” on page 104 for details), copy
anamecgi or anamecgi.exe into your HTTP “executables” directory, and rename it to match

BroadVision, Inc.

Installation and Administration Guide

Chapter 3 Upgrading to Version 4.1
Updating Version 4.0 scripts

27

your installation name [see “Conﬁguring the gateway for a standard CGI server” on page 48 for more
information]:

UNIX

cp $BV1TO1/bin/anamecgi /home/http/cgi-bin/appName

Windows NT cp $BV1TO1/bin/anamecgi.exe D:/InetPub/cgi-bin/appName.exe

For Netscape Enterprise server, update the Netscape conﬁguration to point to the Version 4.1
shared libraries per the instructions in “Conﬁguring the gateway for Netscape Enterprise Server
(NES)” on page 44.

4. Copy the bvsm.cfg ﬁle from the Interaction Manager host to the HTTP host.

On UNIX hosts, the ﬁle is always located in the /etc/opt/BVSNsmgr/ directory.

On Windows NT hosts, the log ﬁle is located in the directory speciﬁed by the
BV1TO1_SESSION_CFG registry key. If the HTTP server and the Interaction Manager are on the
same machine, the location is $BV1TO1_VAR/BVSNsmgr/; otherwise, it is a location that you
deﬁne. See “Conﬁguring the gateway for Microsoft Internet Information Server (IIS)” on
page 46 for details.

5. Repeat Step 3 and Step 4 on each HTTP server host.

6. Shutdown and restart your HTTP server to recognize the changes.

This completes the system conﬁguration migration. If your site has:

l No custom component, dynamic objects, or custom servers, you can start the entire site per the

instructions in “Restarting your site” on page 139.

l Custom Dynamic objects, continue upgrading your site, as described in the next section,

“Updating components and dynamic objects,” described next.

Updating Version 4.0 scripts

In Version 4.1, the BVI_Visitor component has a new interface for locating the visitor by ID. In
Version 4.0, BVI_Visitor.visitor() accepted the visitor name or ID. In Version 4.1, it only
accepts a name, and the new interface BVI_Visitor.visitorByID() is the one to use for
retrieval by ID. For example, in the BroadWay sample application, the daily_quote.jsp ﬁle (in
line 30) had this line:

usermgr.visitor(userid);

In Version 4.1, the call has been replaced with this:

usermgr.visitorByID(userid);

Installation and Administration Guide

BroadVision, Inc.

28

Chapter 3 Upgrading to Version 4.1
Updating components and dynamic objects

Updating components and dynamic objects

If you have created and components or dynamic objects, recompile them against the Version 4.1
libraries.

To update your components or Dynamic Objects to the Version 4.1 library directory:

1. Update your Makeﬁles to include the setting necessary for Version 4.1. See the sample ﬁle for

examples:

UNIX

$BV1TO1/samples/object/dynsample/Makefile.obj

Windows NT $BV1TO1/samples/object/dynsample/object_sample.dsp

Settings to look out for include:

• BV1TO1 (must match that of your Version 4.1 $BV1TO1 environment)

• ROGUEWAVE_INCLUDE (must be the location of your licensed Rogue Wave header ﬁles)

2. Recompile and create the new custom libraries.

3. On UNIX, copy the new component libraries to the Version 4.1 component library directory:

$BV1TO1_VAR/lib/components

4. Copy the new dynamic object libraries to the Version 4.1 dynamic object library directory:

$BV1TO1_VAR/lib/objects

On Solaris, for information about dynamic object shared libraries, see “Component and
dynamic object shared libraries on Solaris” on page 201.

This concludes the migration instructions. To start your One-To-One site, follow the instructions in
“Restarting your site” on page 139.

BroadVision, Inc.

Installation and Administration Guide

4 Setup

29

To conﬁgure and start One-To-One, follow the instructions in this chapter. If you are upgrading your
site from a previous One-To-One version, follow the instructions in “Upgrading to Version 4.1” on
page 17 instead.

To setup your One-To-One site, you need to follow the instructions in:

l Configuring and starting the One-To-One servers described next.

l Configuring and starting the Interaction Manager described on page 40.

l Configuring the HTTP server described on page 43.

l Configuring the Broadway sample application described on page 50.

This chapter describes the conﬁguration steps necessary for starting One-To-One and Interaction
Manager. For detailed information about speciﬁc conﬁguration topics, see:

l Chapter 5, “Server conﬁguration,

l Chapter 6, “Interaction Manager conﬁguration, and

l Chapter 7, “Commerce-speciﬁc conﬁguration.

On Windws NT systems, run all commands in an MKS shell.

Installation and Administration Guide

BroadVision, Inc.

30

Chapter 4 Setup
Overview

Overview

To bring up a One-To-One site, you will perform these general steps. Each of these tasks is described
in greater detail later in this chapter.

1. Install the database management system (DBMS), such as Oracle or SQL Server. See the

documentation included with your DBMS for details. One-To-One will connect to the DBMS as
a client from the root host: the machine where One-To-One is installed. Setup an account the
One-To-One will use to connect to the DBMS [see “Database variables” on page 33 for additional
information]. Test that client host can connect to the DBMS by running the DBMS client software
on the root host.

2. Determine the conﬁguration of your site. For example, are you installing the One-To-One,
Interaction Manager, and HTTP servers on the same machine, or are they each on different
machines? For a production site, you most likely have multiple host machines. Review
“Running a multiple-host conﬁguration” on page 93 before conﬁguring One-To-One if you plan
to run such a conﬁguration.

3. Install the One-To-One software on the root host, as described in Chapter 2, “Installation.” If

you are running a multiple-host conﬁguration, install One-To-One on each machine that hosts
Interaction Manager servers.

4. Setup the environment and start the One-To-One servers, as described in “Conﬁguring and

starting the One-To-One servers” on page 31.

5. Install and conﬁgure the HTTP server. After installing the HTTP server, conﬁgure it to run the

One-To-One gateway application. This application is the bridge between the HTTP and
Interaction Manager servers. Review “HTTP servers and the Interaction Manager” on page 102
for details about how this system works. To setup and conﬁgure the HTTP servers, see
“Conﬁguring the HTTP server” on page 43. You will not be able to completely conﬁgure the
gateway application until you have ﬁnished conﬁguring the Interaction Manager servers.

6. Conﬁgure the Interaction Manager servers, as described in “Conﬁguring and starting the

Interaction Manager” on page 40. If you are running a multiple-host conﬁguration, it is best to
identify the IP addresses of the Interaction Manager machines in the One-To-One conﬁguration,
and then propagate that conﬁguration to the Interaction Manager machines before you conﬁgure
the individual machines. See “Ports and IP addresses” on page 108 for details.

7. Finish conﬁguring the gateway application by copying the Interaction Manager conﬁguration

ﬁle to the HTTP host, as described in “Conﬁguring the HTTP server” on page 43.

8. If you are going to use the Broadway sample application, conﬁgure it for your site per the

instructions in “Conﬁguring the Broadway sample application” on page 50.

9. Start the HTTP server.

The rest of this chapter describes these steps in detail.

BroadVision, Inc.

Installation and Administration Guide

Chapter 4 Setup
Configuring and starting the One-To-One servers

31

Configuring and starting the One-To-One servers

Before you conﬁgure and start the One-To-One services, you must:

l Set up your environment, as described next.

l Conﬁgure One-To-One, as described on page 37.

l Start One-To-One, as described on page 38.

You must use the same user name for configuring and starting One-To-One. You must also use
that same user on all host machines. Additionally, if you are going to run multiple Interaction
Managers, the account needs to be able to rsh from the root host machine: the one where
One-To-One is installed. [See “Remote shell” on page 165 for information about how One-To-One uses
rsh.]

Deﬁning system environment variables

The ﬁrst time you start the One-To-One services, you need to deﬁne several system environment
variables that describe your environment to One-To-One. This section describes those variables.

The One-To-One system requires several more environment variables, but they get deﬁned during
the initial start-up, and then are exported into shell ﬁles that you can source from your shell start-up
script. [See “Shell start-up scripts” on page 39 for information about these ﬁles.]

Script writers can access the One-To-One system variables programmatically with the Request
object. For example, to access the value of the $BV1TO1_VAR variable:

var configDirectory = Request.BV1TO1_VAR

Installation and Administration Guide

BroadVision, Inc.

32

Chapter 4 Setup
Configuring and starting the One-To-One servers

One-To-One variables

Three environment variables describe the One-To-One system location and Orbix object request
broker (ORB) port information:

BV1TO1

BV1TO1_VAR

The directory where you installed the BroadVision One-To-One Enterprise. This
directory is read-only, and may be accessed by multiple development systems.
$BV1TO1 is the One-To-One root directory on the root host, you specified when
installing the services. The count of characters in the value of the $BV1TO1
variable cannot exceed 36.

The directory that contains writable ﬁles, such as the One-To-One conﬁguration
ﬁles and database schema speciﬁcations. If you have separate development and
production systems, each must have its own $BV1TO1_VAR. If this directory
doesn’t already exist, bvconf will create it at start-up.

If you change the local language of your One-To-One system, say from U.S.
English to Japanese, remove your $BV1TO1_VAR/etc/ directory before
starting the system in the new language. The uninstall and installation processes
do not affect the data or ﬁles in the $BV1TO1_VAR directory hierarchy. This
directory hierarchy contains, among other things, the conﬁguration ﬁles for your
system.

IT_DAEMON_PORT Identiﬁes the port number for accessing the ORB. The default is 1221. Change
this value only if you have multiple systems running on the same machine. [See
“Running multiple One-To-One servers on one host” on page92.]

This port, and the IT_DAEMON_SERVER_BASE through
IT_DAEMON_SERVER_BASE+IT_DAEMON_SERVER_RANGE ports need to
be open for Orbix on every One-To-One and Interaction Manager host.

For example, to set the variables to the recommended settings in csh:

setenv BV1TO1 /opt/bv1to1
setenv BV1TO1_VAR /home/bv1to1
setenv IT_DAEMON_PORT 1221

In MKS, sh, or ksh:

export BV1TO1; BV1TO1=D:/bv1to1
export BV1TO1_VAR; BV1TO1_VAR=D:/bv_site
export IT_DAEMON_PORT; IT_DAEMON_PORT=1221

On Windows NT, in previous versions the One-To-One variables were defined as Windows NT
System Properties environment variables. This release does not have that requirement;
additionally, in some configurations, defining them as system properties can cause problems.

BroadVision, Inc.

Installation and Administration Guide

Database variables

Chapter 4 Setup
Configuring and starting the One-To-One servers

33

You also need to provide information about your database management system (DBMS) by setting
the following variables:

BV_DB_VENDOR

(Windows NT only) Identiﬁes the database vendor. It must be either oracle, or
microsoft.

BV_DB_SERVER

Identiﬁes the database server name.

BV_DB_USER

For Oracle, this is the server connection string as deﬁned in the
tnsnames.ora ﬁle; Oracle sometimes calls this the “host”.

The database user-name; the account name that One-To-One will use to
access the DBMS. This account must have permission to create tables and
views, and must be able to create stored procedures. For Oracle, this means
that the account can be assigned connect and resource roles. For Sybase or
SQL Server, the account should have “dbo” privileges.

BV_DB_DATABASE

The database name.

For Oracle, this should the same as value as $BV_DB_SERVER.

For example, in csh::

setenv BV_DB_SERVER smidgen
setenv BV_DB_USER bv_1to1_user_name
setenv BV_DB_DATABASE bv_1to1_db

In MKS, sh, or ksh:

export BV_DB_VENDOR; BV_DB_VENDOR=microsoft
export BV_DB_SERVER; BV_DB_SERVER=smidgen
export BV_DB_USER; BV_DB_USER=bv_1to1_user_name
export BV_DB_DATABASE; BV_DB_DATABASE=bv_1to1_db

Oracle variables

If you are using Oracle,

On UNIX,

• If your site already has a tnsnames.ora deﬁned in /etc, or has the TNS_ADMIN

environment variable deﬁned, comment out the following line in bv1to1.conf ﬁle:

TNS_ADMIN=$getenv(ORACLE_HOME) + "/network/admin"

If you are using Oracle 8 you need to regenerate libclntsh.so — the Oracle client shared
library — to correct problems with the library as it is shipped from Oracle. Otherwise,
One-To-One will fail when starting. To rebuild the file:

a. Edit the $ORACLE_HOME/bin/genclntsh shell script (this script generates

libclntsh.so.

b. Locate the following line in genclntsh and insert a ‘#’ at the start of the line:

ar d $LIBCOMMON sorapt.o
#ar d $LIBCOMMON sorapt.o

# Before
# After

Installation and Administration Guide

BroadVision, Inc.

34

Chapter 4 Setup
Configuring and starting the One-To-One servers

c. Run genclntsh to regenerate the libclntsh.so shared library.

% $ORACLE_HOME/bin/genclntsh

On Window NT:

• On the Windows NT host, install either the Oracle client utilities or the Oracle server
package. You must choose Administrator access in either case to install all of the ﬁles.

• Add an alias for accessing the database. The name you assign to this alias will be used by

One-To-One to access the database. This is the value you will assign to the $BV_DB_SERVER
environment variable.

• To access an Oracle DBMS installed on a UNIX system, install the client utilities on the

Windows NT host. The account for accessing the database must be granted these privileges:

CONNECT
DBA
EXP_FULL_DATABASE
IMP_FULL_DATABASE
RESOURCE
SNMPAGENT

Set $ORACLE_HOME to point to the directory where Oracle ﬁles are installed. On UNIX, the location
is where the Oracle server is located; on Windows NT, it is the location of the Oracle client ﬁles. For
example:

UNIX csh:

setenv ORACLE_HOME /home/oracle/oracle8

Windows NT MKS:

export ORACLE_HOME D:/ORANT

The non-U.S. versions of the bv1to1.conf ﬁle include parameters to identify the character of the
database. These parameters must match the setting used by the Interaction Manager. See “Character
sets” on page 65 for details.

By default, the size of Oracle’s shared memory pool is often not enough to a large One-To-One
installation. To avoid Oracle out-of-memory problems (which can cause data corruption in Oracle’s
shared memory), increase the SHARED_POOL_SIZE in Oracle’s
$ORACLE_HOME/dbs/initOracleServerName.ora ﬁle. Here is an example of the setting in
that ﬁle, you should comment out the SMALL setting and choose at least the MEDIUM value:

shared_pool_size
# shared_pool_size = 6000000 # MEDIUM
# shared_pool_size = 9000000 # LARGE

= 3500000 # SMALL

Your database administrator must make this change, shutdown and restart the Oracle servers before
you start the One-To-One servers. If One-To-One is running and the change must be implemented,
shutdown and restart the One-To-One servers too. You will know if you are having a problem with
the size if you see this level 1 error in the bvlog ﬁle.

Error from Server: ORA-04031: unable to allocate NNN bytes of shared

You can now proceed to conﬁgure and start the services.

BroadVision, Inc.

Installation and Administration Guide

Chapter 4 Setup
Configuring and starting the One-To-One servers

35

Sybase variables

If you are using Sybase,

l Set the $SYBASE variable to the directory where Sybase is installed. For example:

setenv SYBASE /home/sybase/sybase11.0.1

l In non-U.S.A. locales, the SYB_CHARSET parameter in the bv1to1.conf conﬁguration ﬁle
identiﬁes the database character set. This parameters must match the setting used by the
Interaction Manager, as deﬁned in “Character sets” on page 65.

SYB_CHARSET="eucjis"

After setting the environment variables, you can proceed to conﬁgure and start the services.

SQL Server variables

If you are using SQL Server,

l If you intend to use observation logging and loading, the database user performing the loading
must be the database owner (DBO). Only the DBO has the privileges necessary to complete the
loading process, especially adding and dropping tables and stored procedures. The DBO status
can be reassigned to a different user; however, only one DBO can exist per database. Only one
login ID can be the DBO login ID, although other login IDs can be aliased to the DBO.

l In western European locales, when you conﬁgure SQL Server, turn off Automatic ANSI to OEM
conversion, because ISO 8859-1 (referred to as ANSI) is the default SQL Server character set
encoding Windows and Windows NT. To turn off the Automatic ANSI to OEM conversion, use
the SQL Server client utility(\MSSQL\BINN\WINDBVER.EXE)."

l In German locales, turn off the Automatic ANSI to OEM conversion checkbox in the SQL Server

client utility (\MSSQL\BINN\WINDBVER.EXE).

l If you are accessing MSSQL over a local area network, the MSSQL 6.5 client must be installed
before you install One-To-One. To access this setting, use Start | Microsoft SQL Server 6.5 |
SQL Enterprise Manager | Server Name (SQL Server 6.50) | Database | Database Name |
Options. Additionally,

• Set the Truncate Log on Checkpoint setting on development systems to avoid ﬁlling up the

transaction log for the master database.

Set these environment variables:

l $BV_DB_SERVER is the database server name.

l $BV_DB_VENDOR identiﬁes the DBMS vendor. Specify “microsoft”.

For example:

export BV_DB_SERVER; BV_DB_SERVER=hoth
export BV_DB_VENDOR; BV_DB_VENDOR=microsoft

After setting the environment variables, you can proceed to conﬁgure and start the services.

Installation and Administration Guide

BroadVision, Inc.

36

Chapter 4 Setup
Configuring and starting the One-To-One servers

Informix variables

If you are using Informix, set these additional variables:

l $INFORMIXDIR is the directory where Informix is installed.

l $INFORMIXSERVER is the database server name. This corresponds to the $BV_DB_SERVER

variable setting.

l DBMONEY is for German locales, and is deﬁned in the bv1to1.conf conﬁguration ﬁle as:

DBMONEY="DM."

l DBCENTURY is for Informix Year 2000 compatibility. Use the ‘C’ setting for the One-To-One

database, as deﬁned in the bv1to1.conf conﬁguration ﬁle as:

DBCENTURY="C"

For example:

setenv INFORMIXDIR /home/informix
setenv INFORMIXSERVER smidgen

In non-U.S.A. locales, the DBLAN parameter in the bv1to1.conf configuration file identifies
the database character set. See “German Informix (UNIX only)” on page 64 for details.

East Asian locales If you are using Informix in an East Asian locale, before you install the Informix DBMS, specify the
character set for your locale by deﬁning the DB_LOCALE variable as follows.

Japanese

ja_jp.ujis

German

Chinese

de_de.8859-1

zh_tw.big5

Korean

ko_kr.ksc

This variable must be set before you install Informix.

setenv DB_LOCALE ja_jp.ujis

Additionally, before you start One-To-One for the ﬁrst time with bvconf, you must set
CLIENT_LOCALE to the same value. For example:

setenv CLIENT_LOCALE ja_jp.ujis

After setting the environment variables, you can proceed to conﬁgure and start the services.

BroadVision, Inc.

Installation and Administration Guide

Conﬁguring the One-To-One environment and services

Chapter 4 Setup
Configuring and starting the One-To-One servers

37

The default conﬁguration creates a site named bv, and two services named Mall and MyBank. To use
the default, skip this section and go to “Starting the One-To-One servers” on page 38.

All One-To-One conﬁguration information — including environment variable deﬁnitions, site and
service conﬁguration, and load balancing speciﬁcations — is deﬁned in bv1to1.conf, a text ﬁle.
When you run bvconf it looks for the ﬁle in the $BV1TO1_VAR/etc/ directory. If it doesn’t ﬁnd
the ﬁle there, it reads a default ﬁle ($BV1TO1/lib/bv1to1.conf.default) and writes a new
bv1to1.conf to the $BV1TO1_VAR/etc/ directory.

If you are updating your One-To-One installation from a previous release, be aware that this
release contains new configuration settings in the bv1to1.conf file. These settings affect the
configuration of new features, or might affect the configuration of existing features. The
installation process does not alter your existing bv1to1.conf file. If that file exists in the
$BV1TO1_VAR/etc/ directory, the new installation will update the old configuration settings.
To use the new configuration settings, review the old settings and apply any custom changes to
the new bv1to1.conf file.

Treat your bv1to1.conf conﬁguration ﬁle as you would any source code. You might want to
consider putting it into a version control system.

Whenever you make a change to your configuration file, run bvconf syntax_check to test
the validity of the changes before you execute the changes. [See “syntax_check” on page 183 for
more information.]

Creating a new
custom
conﬁguration

The instructions below describe how to conﬁgure One-To-One to get it started. For information
about conﬁguring other aspects of One-To-One, see Chapter 5, “Server conﬁguration.” [See
“bv1to1.conf” on page 161 for information about the conﬁguration ﬁle.]

To change the default conﬁguration before you ﬁrst start One-To-One. From a shell:

1. Create the $BV1TO1_VAR/etc directory:

mkdir $BV1TO1_VAR/etc

2. Copy the default conﬁguration ﬁle to the directory, and rename it as follows:

cp $BV1TO1/lib/bv1to1.conf.default $BV1TO1_VAR/etc/bv1to1.conf

Note there are also Japanese (.jp) and German (.de) versions of these ﬁle in the same location.

3. Make the new ﬁle writable — the default ﬁle is read-only.

chmod u+w $BV1TO1_VAR/etc/bv1to1.conf

4. Make your changes to bv1to1.conf with a text editor.

If you are going to use the Broadway sample application, you must have a service named
“MyBank”. [See “Configuring the Broadway sample application” on page 50 for more information.]

service MyBank { ...

The One-To-One servers are now ready to be started.

Installation and Administration Guide

BroadVision, Inc.

38

Chapter 4 Setup
Configuring and starting the One-To-One servers

Starting the One-To-One servers

To start One-To-One, run bvconf; on UNIX, never run bvconf as the root user. This utility starts,
stops, and provides reports about your One-To-One setup. [See “bvconf” on page 174 for details about
this utility.]

On Windows NT, shut down any running virus checking software. Many virus checkers,
especially McAfee VirusScan, report erroneous messages when starting the One-To-One and
Interaction Manager servers.

Informix users, if you are in an East Asian locale, set the $CLIENT_LOCALE environment
variable before running bvconf. [See “Informix variables” on page 36 for details.]

The ﬁrst time you start One-To-One, use the install_all option to initialize all the databases and
to read the new conﬁguration settings. To start One-To-One from a UNIX or MKS shell:

$BV1TO1/bin/bvconf execute -a install_all

While bvconf is running, it will prompt you to enter the passwords necessary to access your
database management system. You might see other prompts as bvconf conﬁgures and starts the
system, answer them as necessary; most have default answers, or prompts that you can answer
“Yes” to without a problem. Additionally:

l On Windows NT, one prompt asks for the account that One-To-One should use when starting the
servers. This Domain/Account identiﬁer must already exist on this Windows NT host, and
should have the access rights deﬁned in Step 1 of “Installing One-To-One on Windows NT” on
page 14.

l Other prompts will ask you for passwords. One-To-One will remember these passwords for

future use when using these accounts.

On Windows NT, use the password for the Domain/Account or database user.

l Sybase and SQL Server users will see a prompt asking if you want the database log truncated

after the installation. Conﬁrming that prompt will truncate the logs to free up log space. Do this
if you are short of log space in your environment.

Error messages

If you are using a fresh database (one that doesn’t already have One-To-One tables), the following
non-fatal errors might occur. These do not affect the system.

l This error message occurs when bvconf tries to initialize the system tables, and will appear in

the bvlog output:

db_init.syb[11499]@mars:<1>:L1:S05 BV_DBAccessor::BV_DBAccessor
Unable to find accessor in DB schema version table

If bvconf terminates with an error, try to resolve the error from the information in the error
message. You can also examine the log ﬁles in the $BV1TO1_VAR/logs/<hostname>/ directory.

BroadVision, Inc.

Installation and Administration Guide

Shell start-up scripts

Chapter 4 Setup
Configuring and starting the One-To-One servers

39

When you run bvconf execute, it creates script ﬁles that contain commands that set the
environment variables that the other One-To-One servers, utilities, or scripts require. The variables
are all deﬁned in the “Export” section of the bv1to1.conf conﬁguration ﬁle. See “Export
environment variables” on page 163 for details about the variables.

If your application needs an environment variable setting, add the definition to the “export”
section — all definitions in that section get added to the shell start-up scripts.

On Unix, to reference shared libraries not already in the One-To-One system directories, update
LD_LIBRARY_PATH (Solaris) or SHLD_LIBRARY_PATH (HP-UX) to include the path to the
library.

To set up your environment before running the other executables, ﬁrst run one the start-up script
appropriate to your environment. The ﬁlename extension identiﬁes the shell for which the script is
intended. The ﬁles are:

csh:

$BV1TO1_VAR/etc/bv1to1.conf.csh

MKS, sh, and ksh:

$BV1TO1_VAR/etc/bv1to1.conf.sh

Source one of the above files before running any of the One-To-One servers, utilities, or scripts.
Many problems can be avoided when the variables are set correctly. Some of the most common
problems that people encounter are results of issuing commands from terminals that do not
have the variables set correctly.

CAUTION That needs repeating! Source one of the above files before running any of the

One-To-One servers, utilities, or scripts. Many people do not do this and later have problems.
To source the environment:

csh:

source $BV1TO1_VAR/etc/bv1to1.conf.csh

MKS, sh, and ksh:

. $BV1TO1_VAR/etc/bv1to1.conf.sh

On UNIX, because the /bin/sh shell implements both foreground and background jobs in the
same process group, the jobs all receive the same signals, which can lead to unexpected
behavior. It is better to use another job control shell, such as /bin/jsh, for interactive
commands.

Whenever you change the bv1to1.conf ﬁle, restart the One-To-One servers with bvconf
execute to effect the changes, then re-source the shell start-up script before starting the Interaction
Manager servers.

What now?

The One-To-One servers are now running.

l To continue with installation and conﬁguration for the ﬁrst time, proceed to the next section,

“Conﬁguring and starting the Interaction Manager.”

l For detailed instructions about shutting down and restarting the One-To-One services, see

“Shutting down your site” on page 138 and “Restarting your site” on page 139.

l Now is also a good time to read “Recovering after a crash” on page 140 for ideas about

preparing for disastrous system crashes.

Installation and Administration Guide

BroadVision, Inc.

40

Chapter 4 Setup
Configuring and starting the Interaction Manager

Configuring and starting the Interaction Manager

The Interaction Manager is the Web application server. It maintains the connection to the HTTP
server, manages session information, and retrieves and runs scripts and page templates for
presentation to the visitor. This section describes:

l “Conﬁguring the Interaction Manager server,” described next.

l “Starting the Interaction Manager” on page 42.

l “Conﬁguring the HTTP server” on page 43.

l “Troubleshooting Interaction Manager start-up problems” on page 49.

If you are not familiar with HTTP servers, gateway applications, or how they interact with the
Interaction Manager, review “HTTP servers and the Interaction Manager” on page 102 before
continuing.

Conﬁguring the Interaction Manager server

Before you conﬁgure the Interaction Manager:

1. Configure and start One-To-One per the instructions in “Conﬁguring and starting the

One-To-One servers” on page 31.

If you plan to have multiple Interaction Manager hosts, read “Ports and IP addresses” on page 108
for information about the smgr_ip_appName or smgr_first_port_minimum parameters
and how they can ease your conﬁguration activities. If you change either parameter’s
deﬁnition, stop and restart the One-To-One servers with bvconf execute before you conﬁgure
the Interaction Manager.

2. Determine the location of the script root directory. This is where the Interaction Manager looks
for scripts. You must create this directory before starting the Interaction Manager servers. See
“Script root” on page 103 for more information.

3. Determine the gateway application name and relative path to it. When you conﬁgure your HTTP

server, you select the gateway application appropriate to that server, and you choose the
location where the application will reside, relative to the HTTP server’s document root location.
For example, if you put the application in the server’s cgi-bin directory, then the location and
name might be: /cgi-bin/inetcgi.exe. See “Directories and URLs” on page 103 for more
information.

4. Determine your application name. If you are going to use a named application, pick that name

now. An application name identiﬁes the Interaction Manager servers that process requests for
an application. This name appears in the URL address that visitors see in their browsers. [See
“Named applications” on page 104 for detailed information.]

• The ﬁrst time you set up a One-To-One site, it is easiest to not pick a name and to just use the

default which, for the most part, assumes no name.

If you pick a name,

• The ﬁlenames of the Interaction Manager and access control system conﬁguration ﬁles will

be renamed to match the application name. By default, these ﬁles are bvsm.cfg and
bvsm.ACL. See “Conﬁguring access control” on page 55 for more information.

• You will have to use a gateway application that can be renamed to match the application

name. You will do this when you conﬁgure the HTTP server, as described in “Conﬁguring
the HTTP server” on page 43.

BroadVision, Inc.

Installation and Administration Guide

Chapter 4 Setup
Configuring and starting the Interaction Manager

41

5. Make the $BV1TO1_VAR directory accessible to the Interaction Manager servers. If you are

running the Interaction Manager servers on the same ﬁle system as the One-To-One servers, this
is not usually a problem. If the directory is not accessible from the Interaction Manager host, see
“Running a multiple-host conﬁguration” on page 93 for information about cloning the
$BV1TO1_VAR directory.

6. On UNIX hosts, make sure that you have the correct umask settings to allow the conﬁguration
ﬁle to be created with world-read, world-write, and world-search permissions (permission
777). The ﬁrst time you create the control ﬁles they get the same access permission that are in
affect when you run imgr_conf. To ensure that the ﬁle will be created with mode 755:

umask 022

You can now conﬁgure the Interaction Manager servers.

Conﬁguration

Each Interaction Manager installation has a text conﬁguration ﬁle,bvsm.cfg, on the Interaction
Manager host machine. While you may edit the ﬁle directly, it is better to use the imgr_conf utility.
These instructions focus on using that utility to perform the conﬁguration. [For detailed information
about imgr_conf and the bvsm.cfg ﬁle, see “imgr_conf” on page 194 and “bvsm.cfg” on page 190.]

To create or edit the conﬁguration ﬁle:

1. Source the One-To-One environment variables from the appropriate shell conﬁguration ﬁle that

bvconf created [see “Shell start-up scripts” on page 39]. For example:

csh:

source $BV1TO1_VAR/etc/bv1to1.conf.csh

MKS, sh, and ksh:

. $BV1TO1_VAR/etc/bv1to1.conf.sh

2. Run the imgr_conf utility and specify the “conﬁguration” mode.

$BV1TO1/bin/imgr_conf -a configure

This process prompts you for the conﬁguration settings and writes them to the conﬁguration
ﬁle when ﬁnished. The prompts include detailed descriptions of the values they require of you,
and so are not discussed in detail here. (If you haven’t done so already, read “HTTP servers and
the Interaction Manager” on page 102 for a discussion about the topics that are relevant to
conﬁguring the Interaction Manager servers.)

…/BVSNsmgr/

When you are ﬁnished, the conﬁguration ﬁle is located in

UNIX

/etc/opt/BVSNsmgr/

Windows NT

$BV1TO1_VAR/BVSNsmgr/

If after conﬁguring the Interaction Manager, you later change the count of Interaction Manager
engines, IP addresses, or ports, you must:

l If you reduced the engine count, you must stop and then restart the Interaction Manager and

HTTP servers.

l If you changed Interaction Managersettings in the bv1to1.conf file, restart One-To-One with

bvconf execute. Then re-run the Interaction Manager conﬁguration per the instructions
above. That will ensure that bvsm.cfg will have the same engine count.

Installation and Administration Guide

BroadVision, Inc.

42

Chapter 4 Setup
Configuring and starting the Interaction Manager

l If you are running the HTTP and gateway application on a different ﬁle system, copy the

conﬁguration ﬁle from the default location above, to the appropriate location on the HTTP host.

On UNIX, copy the ﬁle to /etc/opt/ on the HTTP host.

On Windows NT, follow the instructions in “Multiple machine conﬁgurations” on page 47.

Stop and restart the HTTP servers to recognize the new conﬁguration.

You are now ready to start the Interaction Manager.

Starting the Interaction Manager

To start the Interaction Manager:

1. In the shell where you plan to start the Interaction Manager, set the One-To-One environment
variables. You can do that by sourcing the appropriate shell conﬁguration ﬁle that bvconf
created [see “Shell start-up scripts” on page 39]. For example:

csh:

source $BV1TO1_VAR/etc/bv1to1.conf.csh

MKS, sh, and ksh:

. $BV1TO1_VAR/etc/bv1to1.conf.sh

CAUTION That needs repeating! Source one of the configuration files before starting any of the
One-To-One or Interaction Manager servers, utilities, or scripts. This is one of the most
common mistakes and failing to do so causes problems starting the site.

2. If they are not already running, start the One-To-One servers

bvconf restart

3. Start the Interaction Manager servers by running the imgr_conf utility

$BV1TO1/bin/imgr_conf -a start

If you are running an named application, include that name, such as this example which starts the
“news” application:

UNIX:

$BV1TO1/bin/imgr_conf -a start -A news

Windows NT:

$BV1TO1/bin/imgr_conf -a start -n news

You can now conﬁgure the HTTP server to connect to the Interaction Manager. For information
about stopping the Interaction Manager, see “Shutting down your site” on page 138.

BroadVision, Inc.

Installation and Administration Guide

Configuring the HTTP server

Chapter 4 Setup
Configuring the HTTP server

43

Do not simultaneously run the same gateway server for One-To-One Version 4.1 and for earlier
versions. Different versions of One-To-One require different server instances.

To conﬁgure your HTTP server for a One-To-One Web site:

1. Make a note of the “gateway application name and relative path to it” that you deﬁned when

you conﬁgured the Interaction Manager servers, such as /cgi-bin/inetcgi.exe. [See Step 3
on page 40 for more information.]

2. Determine which HTTP server and gateway application you will use. [For information about

One-To-One gateways, see “Gateway applications” on page 105.]

3. Conﬁgure the HTTP server to route requests to the gateway application.

Depending on the supported conﬁguration for this release of One-To-One, your choice for
HTTP server is one or more of these:

• Netscape Enterprise Server (NES) running a gateway that is a library which interfaces

directly with NES through NSAPI protocols. Note that each NES HTTP server can support
only one gateway application. This option is not available on all platforms or releases. To use this
option, see “Conﬁguring the gateway for Netscape Enterprise Server (NES)” on page 44.

• Microsoft Internet Information Server (IIS) running a gateway that is a library which

interfaces directly with IIS through ISAPI. This option is not available on all platforms or
releases. To use this option, see “Conﬁguring the gateway for Microsoft Internet Information
Server (IIS)” on page 46.

• Standard CGI server that runs the gateway as an executable. This option usually has the

slowest performance, and as such, is not recommended in a production system. To use this
option, see “Conﬁguring the gateway for a standard CGI server” on page 48.

If you are not familiar with HTTP servers, or how they interact with the Interaction Manager,
review “HTTP servers and the Interaction Manager” on page 102 for a detailed discussion.

Installation and Administration Guide

BroadVision, Inc.

44

Chapter 4 Setup
Configuring the HTTP server

Conﬁguring the gateway for Netscape Enterprise Server (NES)

Never use Netscape’s Admin Server to edit the NES configuration files. If you use that utility
after making the changes described in this section, these changes will be lost and you will have
to manually re-enter them.

To conﬁgure Netscape Enterprise Server (NES) to run the gateway application:

1. Edit the mime.types ﬁle and add this line:

type=magnus-internal/bvc exts=bvc

2. Edit the obj.conf ﬁle and deﬁne the location of the Interaction Manager shared library.

Determine which gateway application library you need. They are located in the
$BV1TO1/lib/nsapi/ directory. These libraries are not interchangeable between versions.

Server

HP-UX

Solaris

Enterprise other than 3.0, such as 2.0 or 3.6.

bvensapi.sl

bvensapi.so

Enterprise 3.0.

bvensapi3.sl

bvensapi3.so

In the obj.conf ﬁle, add the two following Init lines at the end of the “Init” section:

Init fn=load-modules shlib="/opt/bv1to1/lib/nsapi/bvensapi.so"

funcs=bvsm-init,bvsm-process-cgi,bvsm-fake-path

Init fn=bvsm-init application_name="bvsm"

• Do not break any of the lines with a newline; they must be on one line. The lines were broken in

this documentation to ﬁt on the page.

• These settings assume that $BV1TO1 is “/opt/bv1to1”. If One-To-One is installed

elsewhere, edit the path in the shlib parameter accordingly. You may also copy the library
to another location, and then specify that location.

If you are using a named application, change “bvsm” to the application name.

If you are going to use the One-To-One Broadway sample application, edit the bw_start.html
ﬁle and replace the “inetcgi” or “inetcgi.exe” reference with the “bvsm”. See
“Conﬁguring the Broadway sample application” on page 50 for more information.

3. In the beginning of the “NameTrans” section of obj.conf, insert a deﬁnition for the gateway

name.

NameTrans fn="bvsm-fake-path"

gateway_name=/cgi-bin/bvsm redirect="redirect.bvc"

• Do not break any of the lines with a newline; they must be on one line. The lines were broken in

this documentation to ﬁt on the page.

• If you are using a named application, change “bvsm” to the application name.

When you conﬁgure the Interaction Manager, use “/cgi-bin/bvsm” for the location and
name of your gateway program. [See Step 3 on page 40 for information.]

BroadVision, Inc.

Installation and Administration Guide

Chapter 4 Setup
Configuring the HTTP server

45

4. In the beginning of the “Service” section of obj.conf, insert a deﬁnition for the gateway name.

In this example, the name is “/cgi-bin/bvsm”.

Service fn="bvsm-process-cgi" method="(GET|HEAD|POST)"

type="magnus-internal/bvc" gateway_name="/cgi-bin/bvsm"

• Do not break any of the lines with a newline; they must be on one line. The lines were broken in

this documentation to ﬁt on the page.

• Service must precede any entry that services types of the form *~magnus-internal/*

• If you are using a named application, change “bvsm” to the application name.

5. If your NES server is running on a host separate from the one running the Interaction Manager

servers, and both machines do not have access to the same /etc/opt/ directory:

a. Setup and conﬁgure the Interaction Manager servers. This creates the

/etc/opt/BVSNsmgr/bvsm.cfg conﬁguration ﬁle (or “appname.cfg” for a named
application).

b. Copy /etc/opt/BVSNsmgr/bvsm.cfg from the Interaction Manager host to

/etc/opt/BVSNsmgr/ on the HTTP host.

6. Restart the Netscape server (ns-httpd).

• If the HTTP server won’t start, make sure that there is a free socket between the HTTP and

Interaction Manager servers.

You can now connect to a running Interaction Manager server. If a ﬁle news_login.html is
located in the Interaction Manager’s Script root directory, a typical URL for this installation might
look like this (“bvsm” is the default application name):

http://bvsn.com/cgi-bin/bvsm/news_login.html

If the gateway cannot communicate to the Interaction Manager server, it will write an error to its log
ﬁle and the ﬁlename will identify the gateway and the gateway’s process ID, such as
bvsm.nsapi.processId. The log ﬁle is located: in /tmp/BVSNcgi_logs/. Pay attention to log
messages related to problems talking to the Interaction Manager servers. (On UNIX, numeric error
codes are deﬁned in /usr/include/sys/errno.h.) You can ignore “transfer errors” because
they are usually the result of the browser “stopping” the download.

If the HTTP server is unable to access the gateway application, it will write an error to its log ﬁle.,
such as nsloader.log for Netscape servers.

If you encounter any problems connecting to the servers or application, see “Troubleshooting
Interaction Manager start-up problems” on page 49.

Log ﬁles

Installation and Administration Guide

BroadVision, Inc.

46

Chapter 4 Setup
Configuring the HTTP server

Conﬁguring the gateway for Microsoft Internet Information Server (IIS)

To conﬁgure Internet Information Server (IIS) to run the gateway application:

1. Create an executables directory on the HTTP machine to contain the gateway application.

Traditionally, HTTP programs are located in “cgi-bin” (you do not have to use that location;
see “Directories and URLs” on page 103 for more information about this location).

When using the Internet Service Manager utility, a /cgi-bin/ alias might look similar to this
(these pictures are from IIS version 4.0.):

2. Copy $BV1TO1/bin/bvisapi.dll to the HTTP server’s executables directory.

• If you are using a named application, rename bvisapi.dll to appname.dll. When you
later conﬁgure the Interaction Manager, use “/cgi-bin/appname.dll” for the location
and name of your gateway program.

• If you are using the One-To-One Broadway sample application, edit the bw_start.html ﬁle
and replace the “inetcgi” or “inetcgi.exe” reference with the “bvisapi.dll”. See
“Conﬁguring the Broadway sample application” on page 50 for more information.

BroadVision, Inc.

Installation and Administration Guide

Chapter 4 Setup
Configuring the HTTP server

47

3. If your IIS server is running on a host separate from the one running the Interaction Manager

servers, follow the instructions in “Multiple machine conﬁgurations,” below.

You can now connect to a running Interaction Manager server. If a ﬁle news_login.html is
located in the Interaction Manager’s Script root directory, a typical URL for this installation might
look like:

http://bvsn.com/cgi-bin/bvisapi.dll/news_login.html

Log ﬁles

If the gateway cannot communicate to the Interaction Manager server, it will write an error to its log
ﬁle and the ﬁlename will identify the gateway and the gateway’s process ID, such as
bvsm.bvisapi.processId.

On UNIX, the log ﬁle is located in tmp/BVSNcgi_logs/

On Windows NT, the log ﬁle is located in the directory speciﬁed by the BVSNSMGR_LOGS registry
key, described in “Multiple machine conﬁgurations,” below.

If the HTTP server is unable to access the gateway application, it will write an error to its log ﬁle.

If you encounter any problems connecting to the servers or application, see “Troubleshooting
Interaction Manager start-up problems” on page 49.

Multiple machine
conﬁgurations

If your IIS server is running on a host separate from the one running the Interaction Manager
servers:

1. Setup and conﬁgure the Interaction Manager servers. Note the information you provided for
the “gateway application name and relative path to it”, such as /cgi-bin/inetcgi.exe.

2. Determine the location where you want the bvsm.cfg conﬁguration ﬁle to be located, and

create that directory if it doesn’t already exist. For example, d:\BVSNsmgr\ is a good location.

3. Copy the conﬁguration ﬁle from the default location to the directory on the HTTP host.

4. Create two registry keys on the HTTP host. Do that with the Windows NT regedit utility and
with the following steps. Some releases include a script, $BV1TO1/bin/default_setup.reg
that creates the registry entries. If you have that script, edit it to include the locations for your
installation.:

a. If this registry path does not already exist, create it:

\HKEY_LOCAL_MACHINE\SOFTWARE\BroadVision\

One-To-One Application System\4.1\Interaction Manager\
default\export\

If you are using a named application, replace “default” with the name, such as “appname”.

b. Create the registry keys:

BV1TO1_SESSION_CFG — the location and ﬁle you created in Step 2, such as
d:\BVSNsmgr\bvsm.cfg.

BVSNSMGR_LOGS — where the gateway application writes its log ﬁles, such as
d:\BVSNsmgr\logs. Pick a location for your site.

You can now connect to a Interaction Manager server running on a different machine.

Installation and Administration Guide

BroadVision, Inc.

48

Chapter 4 Setup
Configuring the HTTP server

Conﬁguring the gateway for a standard CGI server

To use a standard CGI gateway applications:

1. Create an executables directory on the HTTP machine to contain the gateway application.

Traditionally, HTTP programs are located in “cgi-bin” (you do not have to use that location;
see “Directories and URLs” on page 103 for more information about this location).

a. Create the directory (if it doesn’t already exist).

b. Conﬁgure your HTTP server to run programs from that directory. For example, an HTTP

server’s conﬁguration ﬁle might need a statement similar to this:

Exec

/cgi-bin/*

/home/http/cgi-bin/*

2. Copy the appropriate One-To-One gateway application program from $BV1TO1/bin/ to the

HTTP server’s executables directory.

HTTP Server

Standard CGI, named application ﬁle (ﬁle must
be renamed)

UNIX

Windows NT

anamecgi

aname.exe

Standard CGI, no application name

inetcgi

inetcgi.exe

For example, to use the default gateway on a UNIX HTTP server, copy inetcgi to the
cgi-bin directory:

cp $BV1TO1/bin/inetcgi /home/http/cgi-bin/inetcgi

If you are using a named application, copy anamecgi or anamecgi.exe, and rename it to the
application name. This example for a Windows NT gateway has an application called “news”:

cp $BV1TO1/bin/anamecgi.exe D:/InetPub/cgi-bin/news.exe

• When you later conﬁgure the Interaction Manager, use “/cgi-bin/news.exe” for the

location and name of your gateway program.

3. If your CGI server is running on a host separate from the one running the Interaction Manager
servers, and both machines do not have access to the same exact bvsm.cfg (or “appname.cfg”)
conﬁguration ﬁle:

a. Setup and conﬁgure the Interaction Manager servers. This creates the bvsm.cfg

conﬁguration ﬁle.

b. Copy the conﬁguration ﬁle from the Interaction Manager host to the HTTP host:

On UNIX, copy the ﬁle to /etc/opt/BVSNsmgr/ on the HTTP host.

On Windows NT, follow the instructions in “Multiple machine conﬁgurations” on page 47.

4. If necessary for your HTTP server, stop and then restart the HTTP server.

BroadVision, Inc.

Installation and Administration Guide

Chapter 4 Setup
Configuring the HTTP server

49

You can now connect to a running Interaction Manager server. If a ﬁle news_login.html is
located in the Interaction Manager’s Script root directory, a typical URL for this installation might
look like:

http://bvsn.com/cgi-bin/inetcgi.exe/news_login.html

Log ﬁles

If the gateway cannot communicate to the Interaction Manager server, it will write an error to its log
ﬁle and the ﬁlename will identify the gateway and the gateway’s process ID, such as
bvsm.inetcgi.processId.

On UNIX, the log ﬁle is located in tmp/BVSNcgi_logs/. Numeric error codes in the logs are
deﬁned in /usr/include/sys/errno.h.

On Windows NT, the log ﬁle is located in the directory speciﬁed by the BVSNSMGR_LOGS registry
key. See “Multiple machine conﬁgurations” on page 47 for information about this key.

If the HTTP server is unable to access the gateway application, it will write an error to its log ﬁle.

If you encounter any problems connecting to the servers or application, see “Troubleshooting
Interaction Manager start-up problems” on page 49.

Troubleshooting Interaction Manager start-up problems

If you are having problems starting the Interaction Manager, consider these common oversights:

l Source one of the conﬁguration ﬁles before starting the One-To-One and Interaction Manager
servers. See “Shell start-up scripts” on page 39 for details. This is the most common cause of
problems when starting servers.

l Make sure that the conﬁguration ﬁle and log ﬁle directories have access rights to allow world-
read, world-write, and world-search. Additionally, the conﬁguration ﬁles in the directory must
be at least world-read. Often, these ﬁles are created without this permission because the person
who ran imgr_conf did not have a proper umask setting. The directories

On UNIX are /etc/opt/BVSNsmgr and /tmp/BVSNcgi_logs.

On Windows NT are $BV1TO1_VAR/BVSNsmgr/ on the Interaction Manager machine, and
in the location speciﬁed by the BVSNSMGR_LOGS registry key. See “Multiple machine
conﬁgurations” on page 47 for information about this key.

Pay attention to log messages related to problems talking to the Interaction Manager servers.
(On UNIX, numeric error codes are deﬁned in /usr/include/sys/errno.h.) You can ignore
“transfer errors” because they are usually the result of the browser “stopping” the download.

l Make sure that the Interaction Manager host machine can access the HTTP and One-To-One

server machines.

• Use the UNIX or MKS ping utility to see if the machine can access the other server

machines.

• On the Interaction Manager host, use the Orbix psit utility to test that Orbix is running

and talking to the root host. For example:

$BV1TO1/orbix/bin/psit -h root_host_name

Installation and Administration Guide

BroadVision, Inc.

50

Chapter 4 Setup
Configuring the HTTP server

l If the gateway application cannot communicate to the Interaction Manager server, it will write
an error to its log ﬁle and the ﬁlename will identify the gateway and the gateway’s process ID,
such as bvsm.inetcgi.processId.

On UNIX, the log ﬁle is located in/tmp/BVSNcgi_logs/

On Windows NT, the log ﬁle is located in the directory speciﬁed by the BVSNSMGR_LOGS
registry key. See “Multiple machine conﬁgurations” on page 47 for information about this
key.

l The Interaction Manager engines each write status information to their own log ﬁles in the

$BV1TO1_VAR/logs/<hostName>/ directory.

l The HTTP server error log should normally be small.

l On development systems, if the WWW browser displays an out of date version of a page

template, even though the browser’s caching is turned off, disable the Interaction Manager’s
cache with the tmpl_mgr utility, described in the Installation and System Management System. If
the script is out of date, use the cache_utl utility to disable the script cache, like this:

cache_utl -e script_cache -d disable

See “Maintaining Interaction Managers” on page 154,” for additional tips.

Conﬁguring the Broadway sample application

To use the Broadway sample application, install and conﬁgure One-To-One, the Interaction
Manager, and HTTP servers, per the instructions earlier in this chapter.

This process clears all existing data, if any, already in the One-To-One database. If you have data
that you want to save, back it up before following this procedure. Similarly, if you intend to
install both Broadway and one of the BroadVision One-To-One applications, you must install
Broadway ﬁrst so it doesn’t remove the application database.

When you install One-To-One, the Broadway sample application ﬁles are placed in the
$BV1TO1/broadway directory. To use the sample application, you must:

l copy some of the ﬁles to the HTTP server’s document root location,

l copy some of the other ﬁles to the Interaction Manager script root location, and

l load the sample data into the database.

BroadVision, Inc.

Installation and Administration Guide

Chapter 4 Setup
Configuring the HTTP server

51

The instructions in the rest of this section describe how to do that.

HTTP servers

<doc-root>/

/bw_start.html
/broadway/images/*.gif

Interaction Manager servers

<script-root>/

/broadway/scripts/*.jsp

$BV1TO1/

/broadway/bw_start.html
/broadway/images/*.gif
/broadway/scripts/*.jsp
/broadway/data/*

$BV1TO1_VAR/

/broadway/data/*

Sample data

To conﬁgure and use Broadway:

1. If the Interaction Manager servers are running, stop them now.

imgr_conf -a stop

2. You must have a service named “MyBank” deﬁned in the bv1to1.conf conﬁguration ﬁle.

service MyBank { ...

If this is not already deﬁned in bv1to1.conf, deﬁne it now. See the example in
$BV1TO1/lib/bv1to1.conf.default if you are not sure what to enter.

3. Create the data subdirectory of $BV1TO1_VAR, copy the data into it, and then load the sample
data. This process creates the directory if it doesn’t already exist, and purges the directory if it
does exist. Also, load_data automatically stops and restarts the One-To-One servers.

rm -rf $BV1TO1_VAR/data
cp -r $BV1TO1/broadway/data $BV1TO1_VAR
cd $BV1TO1_VAR/data
./load_data

4. Conﬁgure the Interaction Manager to run Broadway by running the imgr_conf utility in its

“conﬁguration” mode:

imgr_conf -a configure

a. Accept the default application name and default access control ﬁlename.

b. When prompted for the name a location of your gateway program, choose the one that is

correct for your site. The default is “/cgi-bin/inetcgi” or
“/cgi-bin/inetcgi.exe”, which is for a standard CGI server running an un-named
application. If you are using the Netscape or Microsoft HTTP server, or if you are using a
named application, enter that name and location. [See Step 3 on page 40 for more information.]

Installation and Administration Guide

BroadVision, Inc.

52

Chapter 4 Setup
Configuring the HTTP server

• Also, be sure to edit the bw_start.html ﬁle as described in Step 7.

c. When prompted for the start-up scripts directory, make sure to include the

$BV1TO1/script_library directory.

5. The Broadway scripts and data ﬁles are installed by default into $BV1TO1/broadway. The

script root directory should be that location, or it should include links to that location, or you
must copy the directory tree into the script root location. This example copies the tree into the
script root directory:

cp -r $BV1TO1/broadway <script-root>

6. Copy the Broadway images directory into the document root directory (the Broadway scripts

reference the image ﬁles as /broadway/images/...):

mkdir <document-root>/broadway
cp -r $BV1TO1/broadway/images <document-root>/broadway

7. Copy the Broadway login ﬁle, bw_start.html, into the HTTP server’s document root:

cp $BV1TO1/broadway/scripts/bw_start.html <doc-root>/bw_start.html

• If you are not running a standard CGI server with an un-named application, edit the

bw_start.html ﬁle and change the gateway reference from “/cgi-bin/inetcgi” or
“/cgi-bin/inetcgi.exe” to the one correct for your site.

8. If you are using the Verity search feature (available in U.S. English only), generate a Verity

collection:

$BV1TO1/bin/indexer -service_name MyBank -content_name EDITORIAL \

-r <DocRoot> -f $BV1TO1/broadway/data/attrFile -b

9. Shutdown and restart the HTTP server.

10. Start the Interaction Manager server.

To run the Broadway sample application, reference the bw_start.html ﬁle in your browser’s
URL, similar to this:

http://bvsn.com/bw_start.html

When the application starts, if the search page doesn’t work, it is probably because you did not
install, or did not conﬁgure the Verity collections. Note that this feature is not available in Japanese.
[See “Using the Verity search engine” on page 86 for details.]

BroadVision, Inc.

Installation and Administration Guide

5 Server configuration

53

Conﬁguration activities are usually one-time activities that affect how the One-To-One system
operates. The activities in this chapter reﬂect those that you are likely to perform while conﬁguring
the One-To-One servers, including:

l “Naming your site and default service,” described next.

l “Adding, changing or removing a service” on page 54.

l “Changing the “Unclassiﬁed” content label” on page 54.

l “Conﬁguring access control” on page 55.

l “Conﬁguring caching” on page 58.

l “Deﬁning session proﬁle terms” on page 78.

l “Setting the Year 2000 cut-off date” on page 61.

l “Conﬁguring locales” on page 62.

l “Conﬁguring database accessors” on page 66.

l “Conﬁguring visitor notiﬁcations” on page 69.

l “Conﬁguring observation logging” on page 80.

l “Conﬁguring the Matching Agent” on page 81.

l “Setting matching and pricing rule evaluation time” on page 86.

l “Using the Verity search engine” on page 86.

l “Changing the site ID” on page 91.

l “Running multiple One-To-One servers on one host” on page 92.

l “Running a multiple-host conﬁguration” on page 93.

l “Running a multiple-site conﬁguration” on page 95.

For Interaction Manager conﬁgurations, see Chapter 6, “Interaction Manager conﬁguration. For
One-To-One commerce-speciﬁc conﬁguration settings, including shipping, taxing, order numbers,
and payment handling, see Chapter 7, “Commerce-speciﬁc conﬁguration.”

Most of the conﬁgurations in this section require you to edit the bv1to1.conf conﬁguration ﬁle.
For information about that ﬁle, see “Conﬁguring the One-To-One environment and services” on
page 37, and “bv1to1.conf” on page 161. Before you can conﬁgure the One-To-One services, you
must install the software. See Chapter 2, “Installation.” Anytime you change your conﬁguration, be
sure to restart One-To-One. See “Restarting your site” on page 139 for details.

Be sure to back up bv1to1.conf after any configuration changes.

Installation and Administration Guide

BroadVision, Inc.

54

Chapter 5 Server configuration
Naming your site and default service

Naming your site and default service

The default One-To-One conﬁguration creates a site named bv. To change the name, edit the
bv1to1.conf conﬁguration ﬁle and change the name of the site declaration. The name must
contain ASCII characters only. For example, to change the name to InSight:

site InSight {

See “Conﬁguring a multiple-site system” on page 97 for information about deﬁning multiple sites.

To name the services in your site, see the next section, “Adding, changing or removing a service.”
However, if your site will also be maintaining a service, the one that handles overall activities for the
site, change the default_service deﬁnition. For example, to change the name to MyMall:

default_service="MyMall"

Adding, changing or removing a service

To conﬁgure a service on your site:

1. Shut down your site per the instructions in “Shutting down your site” on page 138.

2. Edit bv1to1.conf and add, change, or remove the service’s information. For details about the

conﬁguration information in the ﬁle, see “service” on page 172.

• To add a new service, copy and paste an existing service’s settings, and change the relevant

details for the new service.

• To change a service’s settings, alter the appropriate parameters.

• To remove a service, either delete the service’s details, or comment-out the descriptive lines.

When ﬁnished, save the changes to the ﬁle.

The service name “global” is reserved.

Changing the “Unclassified” content label

In the BroadVision One-To-One Command Center, content that hasn’t been assigned to a category
appears with the label “Unclassiﬁed.” If you want to see a different label, change the
null_category setting of bv1to1.conf. When you make the change and restart One-To-One,
the new label will appear in the Command Center, and all previously “unclassiﬁed” items will have
the new label.

# category management
null_category="Unclassified"

Note that in localized versions of One-To-One, the word “Unclassiﬁed” may already be translated to
the local word.

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Configuring access control

55

Configuring access control

The One-To-One Access Control system determines which scripts, page templates, and dynamic
objects visitors are allowed to run. Additionally, this system can be extended to permit applications
to determine other access rules for other types of information by checking permissions at runtime in
scripts.

To report on the access control specifications in your system, use the acltool or
imgr_acltool utility.

Access control ﬁle When the Access Control system receives a request for a visitor’s access rights, it looks at the

permissions speciﬁed in the site or application access control ﬁle. The ﬁle is usually located in the
same directory as your Interaction Manager’s conﬁguration ﬁle (bvsm.cfg), and has the same
ﬁlename, but with an .ACL extension instead of .cfg. The ﬁlename varies depending on how your
Interaction Manager is conﬁgured. By default, the name is bvsm.ACL, but for a named application,
the ﬁlename is application_name.ACL. See the “Named applications” on page 104 for details
about the names and locations of these two ﬁles.

When you conﬁgure an Interaction Manager for the ﬁrst time with imgr_conf -a configure, it
creates a new file by copying the default version from bvsm.ACL.default in the $BV1TO1/lib
directory.

The ﬁle is structured text that categorizes the permissions by Subjects, and lists the permissions
speciﬁc item within each subject.

Subject

A subject is usually one or more executables, such as a script, template, or dynamic receive object, but
may be other custom application-speciﬁc classiﬁcations. In the control ﬁle, a subject is identiﬁed by
#! followed by the subject name. For example, the scripts subject begins with this line:

#!script

Immediately following the subject is the permission list that speciﬁes the access rules for individual
subject items. For example, the following two permissions allow everyone to access the
bw_init.jsp and bw_login.jsp scripts:

#!script
broadway/scripts/bw_init.jsp
@ALL+
broadway/scripts/bw_login.jsp @ALL+

Access or deny

Each permission is deﬁned on its own line, begins with the Subject item the permission applies to,
and ends with a list of who has permissions and what those permission are. In the examples above,
the two scripts are the subject items, and the @ALL+ gives access permission to everyone. To deny a
permission, use a minus (-) instead of a plus (+) after the Visitor classiﬁer. For example, the following
denies all guests access to the scripts in the members directory:

broadway/scripts/members/*

@guest-

Installation and Administration Guide

BroadVision, Inc.

56

Chapter 5 Server configuration
Configuring access control

Visitor classiﬁer

The visitor classiﬁer identiﬁes who has or doesn’t have permission to the associated Subject. The
following table lists the classiﬁers that the system recognizes.

Visitor classiﬁer

Description

user_alias

Speciﬁc visitor as identiﬁed by the BV_USER.USER_ALIAS proﬁle attribute.

(role)

Visitor currently using the speciﬁed role, as identiﬁed by the
BV_USER_ROLE.USER_ROLE attribute. For information about roles, see the
One-To-One Overview.

[role]

Visitor that has the speciﬁed role, but might not be currently using it.

{community}

@guest

@GUEST

(@all)

[@all]

{@all}

@ALL

Visitor that is a member of the speciﬁed One-To-One Command Center
community. For information about communities, see the Command Center User’s
Guide. Note that when you use a community, the time to evaluate the permission
increases because the Access Control system must ask the Matching System to
determine if the visitor is in the community.

Transient guest (one that does not have a record in the database).

Permanent guest (one that has a record in the database).

All visitors currently using a role.

All visitors that have any role, regardless of whether or not they are using one.

All visitors in any communities. Note that it is possible for a visitor to not be a
member of any the deﬁned communities.

Everybody.

To specify more than one visitor classiﬁer for a permission, separate them with a colon (:). For
example:

.../bw_login.jsp
.../admin_area.jsp
.../partner_area.jsp
.../partner_specials.jsp {value_partners}+:[admin]+:@ALL-

@ALL+
[admin]+:@ALL-
(partner)+:[admin]+:@ALL-

The Access Control system reads the ﬁle from top to bottom, and from left to right until it
encounters a match. As such, it is important to put the most speciﬁc restrictions before the less
restrictive ones in the ﬁle. For example, the following allows partners and administrators to run the
script, but denies it for everyone else.

.../partner_area.jsp

(partner)+:[admin]+:@ALL-

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Configuring access control

57

Subject item

The subject item identiﬁes the executables or custom item that has a permission. Usually the
speciﬁcation is a ﬁlename in a directory, where the directory is relative to the script root, the default
directory where the Interaction Manager looks for executable ﬁles. For example, the following
identiﬁes the partner_specials.jsp ﬁle as being in the broadway/partners/ subdirectory
of the script root directory:

broadway/partners/partner_specials.jsp

@ALL+

The subject item specification is relative to the script root. As such do not begin the speciﬁcation
with a slash (/) because that would tell the system that the ﬁle is relative to the ﬁle system’s root
directory, instead of relative to the script root location.

The subject items are either speciﬁc named items, such as the partner_specials.jsp script
above, or are simple ﬁlename patterns that identify one or more items. To specify a ﬁlename pattern,
use asterisk (*) or question mark (?) wildcards for a string or single character, respectively. For
example, the following uses an asterisk (*) to assign the same rights to all scripts whose ﬁlename
begins with “partner_”:

.../partner_*.jsp

(partner)+:[admin]+:@ALL-

Similarly, you can identify all the ﬁles in a directory, or even all the items in the subject, such as the
last line in the following which denies everyone access to all scripts not speciﬁed above it:

broadway/scripts/members/*
broadway/scripts/partners/* (partner)+:[admin]+:@ALL-
*

@guest-:@ALL+

@ALL-

Remember to be careful about the placement of all asterisk wildcards. For example, the following
denies everyone access to all scripts.

#!script
* @ALL-

While the above example seems a bit silly, consider using this, or the following variation, before you
want to shutdown the site:

#!script
login/* @ALL-

It is a good practice to segregate your application files into directories of common access
permissions. In this way you can blanket assign and deny access to all the files in the directory
using the wildcards. By reducing the size of permissions in the list, you can improve the time
that it takes the Access Control system to determine the permissions for a request.

However, using an asterisk (*) or question mark (?) for a ﬁlename substitution takes the system
longer to evaluate than when using a complete ﬁlename. As such, there is a trade-off in
performance. Generally, fewer items in the permission list using wildcards is faster and less
error-prone than listing every item individually.

Installation and Administration Guide

BroadVision, Inc.

58

Chapter 5 Server configuration
Configuring caching

Configuring caching

One-To-One and Interaction Manager servers use memory caches to improve performance of
activities that access the database, and where the result of computations can be reused for later
evaluations, such as when matching rules ﬁnd content to present to a visitor. All One-To-One caches
contain the most recently accessed items. This section describes how to conﬁgure the caches. See
“Guidelines for using the content cache” at the end of this section for tips using the caches.

The information that can be cached include:

Cache

Used for …

Initial visitor proﬁles

Frequently requested visitor proﬁle information.

Collections

Queries

Content

Categories

Page cache

The parsed results of evaluated Matching system rules.

The IDs of items found as a result of queries.

Deﬁning how many content items to cache.

Recently retrieved categories and categroy content.

Caching the HTML that was generated for page requests; server-side
Javascript code is not cached. See “Conﬁguring the page request
cache” on page 113 for details about this cache.

To empty or reload a cache, use either the Notify Servers command in the One-To-One
Command Center, or the cache_utl utility. The One-To-One Command Center contacts only
those caches that it knows about; the cache_utl utility can access any cache in the site. To
“bind” to the Interaction Manager hosts, it is necessary to open up the Orbix ports in the
firewall for the Command Center machines. See “IT_DAEMON_PORT” on page 32 for details.

Initial visitor proﬁles To improve performance, the Visitor Management database includes a stored procedure that fetches

common visitor proﬁle attributes when the visitor logs in to the site. Change the list of attributes
only if your site requires a different set. Do not include Matching Agent (taxonomy) attributes.

initial_user_profile_attrs = "NAME CITY STATE AGE_RANGE GENDER
INCOME_RANGE NO_HOUSEHOLD MARITAL_STATUS EMPLOY_STATUS
OCCUPATION EDUCATION_LEVEL COUNTRY ADDRESS ZIP"

If you encounter errors about not being able to create the stored procedures, look for extraneous
or erroneous messages coming from the database sever during login. The bvconf utility
recognizes and ignores standard status messages, but if your system has custom messages, it
might cause the creation of the stored procedures to fail.

When you use this setting, bvconf creates $BV1TO1_VAR/get_attr.sql: an SQL script that
deﬁnes the stored procedure which loads the attributes into the cache.

To disable the proﬁle cache, remove or comment-out the initial_user_profile_attrs
deﬁnition in bv1to1.conf, and remove the $BV1TO1_VAR/get_attr.sql script. However, you
will see the following error message when One-To-One starts; you can ignore this message:

"Stored procedure initialization Error 1 in script to

install stored procedure"

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Configuring caching

59

Collections

The Matching system evaluates rules in a Matching collection and keeps the parsed results in a
cache. The rule_cache_size setting deﬁnes the maximum count of rules that are kept in the
cache at any time. For example, the following setting saves 500 rules:

rule_cache_size="500"

Queries

The query cache stores the IDs of items found as a result of a query. The query_cache_size
parameter speciﬁes the maximum count of IDs to store, query_limit limits the count of IDs that
any query can retrieve, and query_cache_timeout speciﬁes how long an ID may remain in the
cache, if it doesn’t get pushed out by another query ﬁrst.

query_cache_size="500"
query_limit="2000"
query_cache_timeout="60" # Expiration time in minutes.

# Count (in thousands) of IDs to store.
# Maximum count of IDs allowed per query.

The generic database cache stores content items found as a result of a query. The
gdb_query_cache_size parameter speciﬁes the maximum count of items to store,
gdb_query_limit limits the count of items any query can retrieve for storage into the cache, and
gdb_query_cache_timeout speciﬁes how long an item may remain in the cache, if it doesn’t get
pushed out by another query.

gdb_query_cache_size="10000"
gdb_query_limit="1000"
gdb_query_cache_timeout="60"

# Maximum count of items to store.
# Maximum count per query.
# Expiration time in minutes.

Content

The content cache settings deﬁne how many content items to keep in the cache. The
default_cnt_cache_size parameter deﬁnes the default size for all content caches. This
example sets all content caches to default to 100 items:

default_cnt_cache_size="100"

You can override the default size for speciﬁc content types using the cnt_type_cache_size
parameter. To set the size for a speciﬁc content type, include the content type’s name — as deﬁned in
the schema speciﬁcation ﬁle for that type — and the count of items to hold. The following example
increases the PRODUCT and AD (advertisement) caches, and turns off caching for the visitor
message scripts (MSGSCRIPT) by setting it to zero:

cnt_type_cache_size="PRODUCT=300, AD=200, MSGSCRIPT=0"

The name of the content must match the CONTENT speciﬁcation in the content type database
speciﬁcation ﬁle. For example, the advertisement content type name is “AD” as deﬁned in
adv_spec.src scheme speciﬁcation ﬁle:

CONTENT: AD "Advertisements"

Previous versions of One-To-One used num_cnt_cache and cnt_cache_sizes parameters
to change the cache sizes. These settings are obsolete as of version 4.0.

Installation and Administration Guide

BroadVision, Inc.

60

Chapter 5 Server configuration
Configuring caching

Choose a cache size that reﬂects the set of contents that you think will be frequently used. For
example, if you have 5000 products, but only about 1000 are frequently asked-for or are targeted by
matching rules, set your cache size to 1000.

The amount of memory that a cache requires is directly proportional to the size of a row of
content data. For example, if each item has a size 1K, specifying a cache size of 1000 requires
around 1MB of memory. Related-attribute lists further increase the amount of memory needed.

Avoid replacing all items in the cache with the results from one large query, by setting
save_member_limit to the maximum count of retrieved items to load into the cache. Similarly, if
a request does not ﬁnd ignore_cache_limit or more items in the cache, the Interaction Manager
requests data from the database instead.

save_member_limit="50"
ignore_cache_limit="5"

Categories

There are two category cache speciﬁcations: cat_cache_size and cnt_type_cache_size for
the CATEGORY_CONTENT content type.

Because One-To-One deﬁnes categories as a type of content you can deﬁne the count of categories to
cache with the cnt_type_cache_size deﬁnition:

cnt_type_cache_size="CATEGORY_CONTENT=100, AD=200, MSGSCRIPT=0"

The content cache holds the category item plus any data in that row in the BV_CATEGORY table.
The above example caches 100 rows of category content.

The cat_cache_size parameter speciﬁes the count of categories to retain. Actually, it is the count
of IDs of the category content items in the path to a speciﬁc item. For example, for the path
“/Automobiles/Sedans/German/Mercedes”, the cache stores the ID of the Mercedes category
content item, plus the IDs of the Automobiles, Sedans, and German category content items.

It is useful to adjust this cache if the application uses objects that will jump around in the tree, as
opposed to normal traversing of categories trees. Then, for best results, set the cache size about one
quarter ( 1/4 ) of total count of categories. This example stores 625:

cat_cache_size="625"

When category matching retrieves more than match_cat_preload count of items, the system will
load all of that category’s items into the cache; it does this by making one SQL query to retrieve the
items. For queries that retrieve less than match_cat_preload count items, the system makes one
SQL request for each item. For example, when the limit is set to 50, a query that returns 49 random
items make 49 separate queries. But a request of 100 random items results in one query that retrieves
all the items in the category.

match_cat_preload="50"

Guidelines for using the content cache

Here are some important topics to be aware of when using the content caches:

l Because the cache is an in-memory store, it is possible for the items in the cache to be

inconsistent with the data in the database. For example, if someone uses the One-To-One
Command Center to change the price of a product, the price gets updated in the database, but
not in the cache. When updating data in the database, use one of the cache ﬂushing mechanisms

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Setting the Year 2000 cut-off date

61

to ensure that important out-of-date information gets removed from the cache. To ﬂush a cache,
use the cache_utl utility, the Notify Servers command in the One-To-One Command Center, or
one of the program interfaces, such as flush_one_content().

l If you are doing updates on many content items in a sequence, it is better to ﬂush the cache for

the whole content type as oppose to ﬂushing each individual content item.

l If your content is rapidly changing (such as for stock prices), it is better to turn the cache off. The

overhead of frequently loading the cache is a big performance impact.

l Only content items retrieved by their content key or content OID are cached, such as from the

results of matching rules; the results of ad-hoc queries are not cached.

l If you are not using a content type, set its cache size to zero to free up memory for other caches.

l Only content that visitors can see should be cached: items that are not visible, such as items that
are off-line, should not be cached. Do not waste memory by ﬁlling a cache with content that the
visitor cannot see. Note that if you have rules that can load off-line data, it is better to take the
rule off-line so that it does not load the data, than to turn each of the data items off-line.

l If you have content with related-attribute lists, the list entries for a content are not cached until

they are accessed.

l Avoid caching very large content items (such as content with large text blobs). Instead of using
Text columns, it is better to store large text in the ﬁle system, and have a column that identiﬁes
the ﬁlename instead.

l To report the count of accesses to the content database, use bvconf monitor, like this:

% bvconf monitor -m BV_DB_STAT -p cntdb

l To manage the page template cache, use the tmpl_mgr utility. For all other caches, use the

cache_utl utility. For example, to flush scripts and page templates:

cache_utl -e script_cache -d flush

Setting the Year 2000 cut-off date

By default, One-To-One converts all two-digit years from 00 up to and including 29 to be in the
2000s, all others are assumed to be in the 1900s. To change that year, change the BV_Y2K_CUTOFF
setting. The default is 30, which means that "30" and later are assumed to be 1930 or later.

# Year 2000 2-digit to 4-digit conversion
BV_Y2K_CUTOFF="30"

The BV_Y2K_CUTOFF setting does not affect date conversions in the One-To-One Command Center
because that application uses the conversion routines supplied by the Windows operating system,
and that system (Windows 95) always assumes 30 as the cut-off year. Because the One-To-One
Command Center and One-To-One system can have potentially different cut-off dates, it is possible
that a date string entered in the One-To-One Command Center would be converted different from a
date string entered in an application. You can avoid this problem by either not setting
BV_Y2K_CUTOFF above 30, or by always entering ambiguous One-To-One Command Center dates
as four-digits. When communicating with the One-To-One servers, the One-To-One Command
Center always uses already converted date-time values.

Installation and Administration Guide

BroadVision, Inc.

62

Chapter 5 Server configuration
Configuring locales

Configuring locales

In One-To-One, a system’s locale affects the characters, currency symbols, and date/time format
displayed to Web visitors and Command Center users. When you install One-To-One for a U.S.
English or Japanese locale, the installation process creates a default bv1to1.conf ﬁle that
conﬁgures the One-To-One servers and Command Center for that locale. (For German locales, copy
the bv1to1.conf.de ﬁle to $BV1TO1_VAR/etc/bv1to1.conf.) However, you might still need
to ensure that the database and Interaction Manager servers are conﬁgured to match. For other
locales, you might need to deﬁne the conﬁguration for all of the settings.

If you change the local language of your One-To-One system, say from U.S. English to Japanese,
remove your $BV1TO1_VAR/etc/ directory before starting the system in the new language.
The uninstall and installation processes do not affect the data or files in the $BV1TO1_VAR
directory hierarchy. This directory hierarchy contains, among other things, the configuration
files for your system.

Character sets deﬁne how character values map to character symbols. “Character sets” on page 65
describes how to conﬁgure character sets for a One-To-One site.

One-To-One formats currency and date/time values, and determines currency symbols as follows:

l The One-To-One servers do not format values for display, and they do not sort lists of items.

However, the database management software (DBMS) often sorts lists, either automatically or
at the request of the caller, and that sorted list is passed to the caller. See the documentation for
your DBMS for details about conﬁguring it.

l The Command Center formats data and sorts items for display based on the format deﬁned by
the Microsoft Windows environment on which it is running. You may specify a different
currency symbol with the intl_currency (lower case) parameter in the bv1to1.conf ﬁle.

l The Interaction Manager, components, and e-mail notification servers, formats currency,

date/time, and numeric values, and sort lists of items based on the default locale for the site.
The default locale should be deﬁned by the BV_LC_LIST parameter. To sort lists of items, these
systems rely on the collation sequence deﬁned by the operating system locale.

• On UNIX, they look for LC_COLLATE, and if it is not deﬁned, they look in LC_ALL, and then

LANG to determine the sort order.

• On Windows NT, the system looks in the LC_ALL environment variable, which is deﬁned in

the bv1to1.conf ﬁle.

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Configuring locales

63

These bv1to1.conf ﬁle parameters deﬁne the locales and formatting that the system uses. Most
are obsolete; try to use BV_LC_LIST and intl_currency only.

Parameter

Description

BV_LC_LIST

List of locales, up to 64, to use for determining the currency format and symbols, and
for date/time formatting. The ﬁrst locale in the list is the default for the site.

On UNIX, When this is deﬁned, BV_LC_MONEY is ignored if it too is deﬁned. If this
parameter is not deﬁned, the servers use the information deﬁned by
LC_MONETARY and LC_TIME, and if they are not deﬁned, the servers look in
LC_ALL and then LANG to get the settings.

On Windows NT, If this parameter is not deﬁned, the servers use the information
deﬁned by LC_ALL.

BV_LC_MONEY

(UNIX only) Set the currency and date/time locale. This parameter will be obsolete in
a future release so avoid using it; use BV_LC_LIST to set the default locale.

INTL_CURRENCY (Upper case, UNIX only, obsolete parameter) Overrides the default currency code

intl_currency

for the site. Setting this parameter might have unexpected results, so avoid using it;
use BV_LC_LIST to set the default locale.

(lower case) Currency code for Command Center to display. This parameter tells the
Command Center what currency code the servers are using. For example, this sets
the code to “USD” for U.S. Dollars:

intl_currency="USD"

If this parameter is not deﬁned, the Command Center uses the symbol for the locale
of the Windows machine on which is it running.

INTL_PRECISION (UNIX only, obsolete parameter) Overrides the count of decimals digits to display in

currency. Setting this parameter might have unexpected results, so avoid using it;
use BV_LC_LIST to set the default locale.

LC_ALL

Deﬁnes the system locale that One-To-One defaults to for locales not deﬁned by
other parameters in this table.

Here is a partial list of some common locales, currency codes, and whether or not the locale is part of
the European Union (EU).

Windows NT Solaris

HP-UX

Currency code Part of EU

Country

Austria

Britain

Denmark

Finland

France

Germany

Greece

Ireland

Italy

Japan

Korea

dea

eng

dan

ﬁn

fra

deu

ell

ita

jpn

kor

de_AT

en_UK

da

su

fr

de

en_GB.roman8

da_DK.roman8

ﬁ_FI.roman8

fr_FR.roman8

de_DE.roman8

el.sun_eu_greek

el_GR.greek8

en_IE

it

ja

ko

it_IT.roman8

ja_JP.eucJP

ko_KR.eucKR

nl_NL.roman8

pt_PT.roman8

ATS

GBP

DKK

FIM

FRF

DEM

GRD

IEP

ITL

JPY

KRW

BEF

NLG

PTE

Y

N

N

Y

Y

Y

N

Y

Y

N

N

Y

Y

Y

Lux/Belgium frb or nlb

fr_BE or nl_BE

Netherlands

Portugal

nld

ptg

nl

pt

Installation and Administration Guide

BroadVision, Inc.

64

Chapter 5 Server configuration
Configuring locales

Country

Spain

Sweden

Taiwan

U.S.A.

Windows NT Solaris

HP-UX

Currency code Part of EU

esp

sve

es

sv

es_ES.roman8

sv_SE.roman8

zh_TW.big5

zh_TW.big5

enu or usa

en_US

en_US.iso88591

ESP

SEK

TWD

USD

Y

N

N

N

Most UNIX systems default to the traditional C locale. Unless you are running a U.S. English
site, you will most likely want to change this to your locale. To see a list of the locales your
system recognizes, use the locale -a UNIX command.

On UNIX, to support the euro, you will need to obtain the patches from the UNIX vendor to support
the ISO8859-15 character set. For example, to recognize EUR as a valid currency on Solaris, you
might use “de.ISO8859-15@euro”; on HP-UX you might use “de_DE.iso885915@euro”.

Setting locales

Set your system’s locale or locales with the BV_LC_LIST parameter. This parameter deﬁnes a list of
locales recognized by your system. The ﬁrst locale is the default for your site, and is likely to be all
that you need to deﬁne. Include more than one locale when your site needs to recognize multiple
locales, such as when the site supports multiple currency codes.

On UNIX:

These two examples — the ﬁrst for Solaris and the second for HP-UX — make UK English the
default for the site, but include other locales as well:

BV_LC_LIST="en_UK,de,fr,it"

# Solaris

BV_LC_LIST="en_GB.iso88591,de_DE.roman8,ja_JP.eucJP"

# HP-UX

To include euro in addition to country-speciﬁc currency display, include both locales in the list.
For example, this deﬁnition for Germany includes both locales:

BV_LC_LIST="de,de.ISO8859-15@euro"

On Windows NT:

This example makes UK English the default locale for the site, but includes other locales as well:

BV_LC_LIST="eng,usa,sve"

In your application, you can format a currency display for a particular value by specifying one of
the locales in the BV_LC_LIST. This is very useful for sites that need to display multiple currency
formats to a visitor from one page. To format currency in an application, call the bv_make_money()
function. See the API Reference for details about this function.

German Informix
(UNIX only)

For sites using Informix with a German locale setting, you must also set the $DBMONEY environment
variable to the correct currency symbol. For German locales, the default bv1to1.conf
conﬁguration ﬁle includes this setting:

DBMONEY="DM."

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Configuring locales

65

Some characters are reserved characters in a particular shell. To use them, “escape” the character by
enclosing the value in single quotes ('). For example, to assign a US dollar sign ($):

DBMONEY='$.'

See “Informix variables” on page 36 for information about other Informix-speciﬁc settings.

Character sets

A character set deﬁnes which character symbols to display for each character of data; it maps values
to symbols. The database, Command Center, and Interaction Manager HTML page generation
server must be set to the same character set. In a One-To-One site, you deﬁne these mappings by:

1. Deﬁning the database character set when you create the database. The character set must be the
same set as used by the Command Center and Interaction Manager servers. See your database
management system’s documentation for details about deﬁning the set.

On UNIX in western European locales, when you conﬁgure SQL Server, turn off Automatic ANSI
to OEM conversion, because ISO 8859-1 (referred to as ANSI) is the default SQL Server
character set encoding Windows and Windows NT. To turn off the Automatic ANSI to OEM
conversion, use the SQL Server client utility(\MSSQL\BINN\WINDBVER.EXE)."

2. Identifying the database character set in Export environment variables section of the

bv1to1.conf ﬁle. Each DBMS has its own parameter [for more information about these parameters,
see “Database variables” on page 33].

DBMS vendor

Variable

Example

Oracle

Sybase

Informix

NLS_LANG

NLS_LANG="japanese_japan.ja16euc"

SYB_CHARSET

SYB_CHARSET="eucjis"

DBLANG

DBLANG="en_US.8859-1"

SQL Server

None.

—

3. Deﬁning the character set used by the Interaction Manager when generating the HTML to send
to the visitor’s browser. Netscape and Microsoft browsers display documents in the speciﬁed
character set when the corresponding fonts are installed on the browser’s system.

To deﬁne the set, run imgr_conf -a configure and declare a character set when prompted.
The character set must be the same as the database setting deﬁned in Step 2. The Interaction
Manager embeds the speciﬁcation in the header of all HTML pages it generates, similar to this:

Content-type: text/html;charset=iso-8859-1

4. Deﬁning the mapping of database data to the Command Center. The encoding_type and
ISOCharSet parameters in bv1to1.conf tell the Command Center how to map the data.

• encoding_type tells the Command Center how to convert the characters coming from the
database. The value for this parameters is usually MBCS (multi-byte character set) or EUC.

Installation and Administration Guide

BroadVision, Inc.

66

Chapter 5 Server configuration
Configuring database accessors

• ISOCharset tells the Command Center to use Internet Explorer to perform character

conversion of the characters from the database. When this parameter is deﬁned,
encoding_type parameter is ignored. Internet Explorer version 3.0 or greater must be
installed on the Command Center machine.

Server and database
character set

encoding_type
parameter

ISOCharSet
parameter

Language

Arabic

Hebrew

Japanese

Korean

Turkish

iso-8859-6

windows-1256

Central European

iso-8859-2

windows-1250

Chinese, Traditional

big5

English
(Western European)

windows-1252 and
iso-8859-1 are identical

MBCS

MBCS

MBCS

MBCS

MBCS

MBCS

MBCS

MBCS

EUC

MBCS

iso-8859-8

windows-1255

euc-jp

shift-jis

euc-kr (KCS 5601-1987) MBCS

windows-1254 and
iso-8859-9 are identical

MBCS

iso-8859-6
windows-1256 1

iso-8859-2
windows-1250 1
big5 2
windows-1252 1 or
iso-8859-1 3

iso-8859-8
windows-1255 1
euc-jp 2
shift-jis 2
euc-kr 2
windows-1254 1 or
iso-8859-91

1 This setting is optional when the encoding_type parameter is deﬁned.
2 This setting is not required; use encoding_type instead.

Configuring database accessors

One-To-One connects to its database through database accessor servers. These servers form the SQL
requests that get sent to the underlying database management system (DBMS). The accessors are:

l Content accessor (cntdb) handles requests and updates of One-To-One content. This accessor

calls the external accessor when it needs to communicate to an external database.

l Proﬁle accessor (cmsdb) handles visitor proﬁle requests and updates. This accessor calls the

external accessor when it needs to communicate to an external database.

l Generic accessor (genericdb) handles content query requests from the One-To-One Command

Center and from applications, when speciﬁcally called from the application.

l External accessor (extdbacc) handles requests and updates of content and proﬁles to external

databases: ones that are not part of the One-To-One database. The external accessor that comes
with One-To-One knows how to communicate to the same DBMS systems that One-To-One
knows about. For example, if your One-To-One database is Oracle, you can connect to an
external Sybase or SQL Server database because it is supported by this release. To connect to
other DBMS systems, you need to implement that accessor per the instructions in the API
Reference.

Conﬁguration
parameters

To connect to a DBMS, the accessors need conﬁguration information. Some of the information
includes the database environment variables: $BV_DB_SERVER, $BV_DB_USER, and
$BV_DB_DATABASE. (Other variables are speciﬁc to the DBMS and are discussed in “Database
variables” on page 33.)

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Configuring database accessors

67

When you conﬁgure One-To-One with the bvconf utility, that utility gets and sets the database
conﬁguration information from two places in the bv1to1.conf conﬁguration ﬁle. First, in the
“deﬁnitions” section of the ﬁle, bvconf retrieves the environment variables settings and stores
them to bv1to1.conf parameters.

bv_dbserver=$getenv(BV_DB_SERVER)
bv_database=$getenv(BV_DB_DATABASE)
bv_dbuser=$getenv(BV_DB_USER)

After getting the database settings from the environment variables, bvconf prompts the database
password:

bv_db_passwd=$noecho("Enter DB password: ")

The $noecho function prompts you for the password and encrypts the value. Later, the accessor
decrypts the password before sending it to the DBMS. If you have an external database accessor, use
$noecho to retrieve the ext_dbpassword value.

ext_dbpasswd=$noecho("External database password: ")

After it has retrieved the above information, bvconf is able to determine additional information
and write some of it to variables deﬁned in the “Export” section of bv1to1.conf. Most notable is
the $BV_DB_LIB and $BV_DB_LIB_PATH values. These point to the DBMS library that the accessor
connects to. In a standard conﬁguration, the bvconf utility deﬁnes these variables for you.

dbserver=$arg(bv_dbserver)
database=$arg(bv_database)
dbuser=$arg(bv_dbuser)
password=$arg(bv_db_passwd)
dblib=$getenv(BV_DB_LIB)

# database server
# database name
# database account
# encrypted password
# database library

However, if you are using an external database accessor, you will need to deﬁne and extend these
deﬁnitions for each process. [See “External database accessors,” below, for details.]

Idle reconnect

If a database server is idle for a speciﬁed period of minutes, the accessors will disconnect and
reconnect to it. The default wait is 30 minutes. You can change this period with the
max_idle_time parameter:

max_idle_time="30"

Deﬁning
processes

One-To-One launches servers as processes, which are deﬁned in the bv1to1.conf ﬁle. In the
simplest form, the process deﬁnitions look like this:

process cmsdb {}
process cntdb {}
process genericdb {}

Like all processes, you deﬁne them in the Site section of the bv1to1.conf ﬁle. You can deﬁne them
globally for the site, or speciﬁcally for a group of services within the site. See “group” on page 172
for an example of a group-speciﬁc deﬁnition.

Installation and Administration Guide

BroadVision, Inc.

68

Chapter 5 Server configuration
Configuring database accessors

Each database accessor, by default, uses the database parameters deﬁned above (dbserver,
database, dbuser, password, and dblib). For example,

process cmsdb {}

is the same as

process cmsdb { parameter

dbserver=$arg(bv_dbserver)
database=$arg(bv_database)
dbuser=$arg(bv_dbuser)
password=$arg(bv_db_passwd)
dblib=$getenv(BV_DB_LIB)

}

Two additional parameters are host and diagnostics. These parameters identify the host machine on
which to run the accessor, and the message level to write to the log ﬁles, respectively.

process cmsdb { parameter

host = "mars"
diagnostics = "1"

# run it on the mars host
# log Orbix errors messages only

}

External database
accessors

For external accessors, there are additional or different parameters that you must deﬁne. An external
accessor interacts with a database different from the One-To-One database. That database can be
running on the same DBMS as the One-To-One database, or another DBMS. If the DBMS is not one
that One-To-One supports, you will need to develop a custom database accessor (see the API
Reference for details about creating ).

At the site level, you can specify whether or not external databases should be read-only or can be
updated with the external_profile_write and external_content_write parameters.
Each accessor can then override the site-level deﬁnition by including a write_protect parameter.

external_profile_write="0"
external_content_write="1"

# Profiles are read-only
# Content can be updated

Here are the parameters that are recognized by the external database accessor processes:

Parameter

Description

ext_accmethod

Name of the CORBA server that implements the external accessor. For One-To-One
supported DBMSs, use “bv_default”.

ext_datasource

External accessor name. This must match the name that you use in the data_source
parameter in the database schema. See the Database Administrator’s Guide for
details about conﬁguring the schema for an external database.

Use “extdbacc” to access a DBMS that this version of One-To-One supports.

ext_dbname

Database name. For Oracle, this value must be empty.

ext_dbpassword Password used to access the database. You can prompt for this when bvconf runs by
using the $noecho() function [see“Conﬁguration parameters” on page66 for amd
example].

ext_dbtype

Type of the DBMS.

On UNIX, the valid names are “oracle”, “sybase”, and “informix”.

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Configuring visitor notifications

69

Parameter

Description

ext_dbserver

ext_dbuser

Database server name. For Oracle installations, this is the server connection string as
deﬁned in the tnsnames.ora ﬁle.

Account name used to access the database. This account must have permission to
create tables and views, and must be able to create stored procedures.

ext_lib

Oracle: the account can be assigned connect and resource roles.

Sybase and SQL Server: account should have “dbo” privileges.

Informix: the database user must be the same account that conﬁgures One-To-One.

DBMS library for an external database accessor. You must include this parameter if
you are using a DBMS other than the one used for the One-To-One database. After
naming the library with this deﬁnition, you should include a link to this library in the
$BV1TO1/lib directory. For example, if your One-To-One database is Sybase, and
your external database is Oracle, add a link in $BV1TO1/lib that points to Oracle’s
libclntsh library.

ext_writeprotect When set to “0”, the database can be updated; otherwise; when “1”, the database is
read-only. This overrides the external_profile_write and
external_content_write deﬁnitions.

For example:

process extdbacc {

parameter

ext_datasource="Customer accounts"
ext_dbuser=$arg(bv_dbuser)
ext_dbpassword=$arg(bv_ext_passwd)
ext_dbserver="smidgen"
ext_dbname="CUST_ACCTS"
ext_dbtype="oracle"

}

Configuring visitor notifications

Visitor notiﬁcations are messages that are sent or delivered to registered visitors. Each message can
be personalized to the visitor, and is generated by a JavaScript script that is run at a scheduled time.
The schedules can be run once, or run periodically, as deﬁned in the One-To-One Command Center.
Additionally, the messages can be delivered to an “inbox” where the visitor can retrieve the message
the next time they log in to the site, or they can be sent by some other means, such as e-mail, fax, or
pager. The release of One-To-One includes support for the e-mail delivery mechanism only, though
you can implement and include the others through custom development work.

There are two kinds of visitor notiﬁcations

l Alerts are messages that visitors request to inform them when an event has occurred. Your site’s

application must provide the mechanism for the visitors to choose the alerts they desire.
Additionally, you must implement a means for the alert to recognize when the requested event
has occurred, and then schedule the message generation and delivery. The One-To-One
Command Center user determines when and how often the schedule should be run.

l Targeted messages are ones that the site sends to a community of visitors. The community is
deﬁned by the One-To-One Command Center user, who also deﬁnes the schedule of when to
generate and send the messages, and how often this should occur.

Installation and Administration Guide

BroadVision, Inc.

70

Chapter 5 Server configuration
Configuring visitor notifications

This section describes how to conﬁgure your site to generate and deliver visitor notiﬁcations.,
including:

l “Notiﬁcation process” on page 70

l “Message scripts” on page 73

l “Messages” on page 73

l “Processes and daemons” on page 74

For information about:

l Deﬁning schedules, messages, and communities, see the Command Center User’s Guide.

l Creating the means for visitors to select the alerts they wish to receive, see the Developer’s Guide

to Components and Scripts.

l Creating alert plug-ins and new delivery mechanisms, see the API Reference.

Notiﬁcation process

To generate a deﬁned and scheduled notiﬁcation, the notiﬁcation system follows these steps:

1. Notiﬁcation schedules are deﬁned in the BV_ALERTSCHED and BV_MSGSCHED tables. They are

deﬁned by the One-To-One Command Center user or by an application.

2. The schedule poller (sched_poll_d) scans the tables to determine when a notiﬁcation must be
run. When it ﬁnds one that needs to be run, it notiﬁes the schedule server. The poller ignores
jobs that are currently running, and skips schedules that have been missed. For example, if a job
is scheduled to run periodically at 05:00, 06:00, 07:00, and 08:00, but the scheduler process
doesn’t start until 07:30, it immediately runs the 05:00 job, and then sets the next scheduled job
to be the one at 08:00, and skips the 06:00 and 07:00 schedules.

3. The schedule server (sched_srv) creates the messages. If the message is destined for a visitor’s
inbox, it puts the message in the BV_ALERT_INBOX table, updates the BV_ALERT_SPEC table
(if the message is an alert, it does not add duplicate messages if the alert_type is conﬁgured
that way). Otherwise, it writes the message to a ﬁle in the pending branch of the
msg_not_completed limb of the bv_schedule_msg_dir directory tree. [See the illustration
on page 71 for details about the directory structure.] It then generates the message or messages.

• For personalized (dynamic) messages, the schedulers generate one message for each visitor
in the target community. The scheduler servers generate the messages into one or more
directories — each directory holds up to bv_schedule_dynamic_msgcount count of
messages — by balancing the count of messages in each directory.

For example if bv_schedule_dynamic_msgcount is deﬁned as 500, and there are 10000
visitors in the target community, the servers create 20 directories.

• For non-personalized (static) messages each scheduler creates one message, and a list of
visitors to receive the message. Later, the delivery servers retrieve each visitor’s address
from the list and combine it with the message. Depending on the count of visitors in the
target community and the value of the bv_schedule_static_msgcount parameter, the
schedulers generate one or more address list and message ﬁles. Each address list holds up to
bv_schedule_static_msgcount count of addresses. For each delivery server there is
one copy of the static message ﬁle.

For example if bv_schedule_static_msgcount is deﬁned as 2,000, and there are 10,000
visitors in the target community, the servers create 5 address list and message ﬁles.

When the schedule server ﬁnishes a job, it writes a status ﬁle to the job’s directory under the
msg_not_completed limb. The ﬁlename is either “gen_complete” or “gen_failed”. The

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Configuring visitor notifications

71

later ﬁle is created if any of the job’s messages were not generated — and they should have
been. All messages that were generated get processed, regardless of whether or not all messages
were generated.

4. The delivery servers (such as deliv_smtp_d) poll their directories in the pending branch of
the msg_not_completed limb looking for messages to process. They attempt to deliver all
messages found in their directories.

• For personalized (dynamic) messages, the server attempts to deliver each message to its

intended recipient. When ﬁnished, if a message cannot be delivered, the server moves the
messages from the pending branch to the sent_failed branch. Then, the server either
moves the directory of successfully sent messages to the sent_success branch, or deletes
the directory, depending on the bv_schedule_keep_messages ﬂag.

• For non-personalized (static) messages, the server attempts to deliver a copy of the message
to each address in the address list. When ﬁnished, the server moves the address list from the
pending branch to the sent_success branch, or deleted, depending on the
bv_schedule_keep_messages ﬂag in bv1to1.conf. For failed deliveries, the address
of the failure is appended to the address list in the sent_failed branch.

5. The delivery completion server (deliv_comp_d) scans the job directories under the

msg_not_completed limb looking for the gen_complete and gen_failed ﬁles. It then
moves the message ﬁles from the msg_not_completed limb into either the msg_completed
or msg_failed limbs. It then updates the BV_MSGSTAT or BV_ALERTSTAT tables with the
statistics about the job.

Messages are placed in the message directory tree for processing. The root directory for the
generated messages is deﬁned by bv_schedule_msg_dir, which by default is deﬁned to be
$BV1TO1_VAR/messages/ directory:

bv_schedule_msg_dir=$getenv(BV1TO1_VAR) + "/messages"

Here is a map of the message directory tree:

bv_schedule_msg_dir

/msg_failed/

/msg_not_completed/

/msg_completed/

One for each job.

Job directories

/bv_web_alert/

In this limb only.

/sent_success/

/pending/

/sent_failed/

One for each delivery type,
such as e-mail or fax.

Delivery mechanism directories

One for each
dynamic_msgcount
count of messages.

Message directories

Dynamic messages

Address list and
static message

One for list for each
static_msgcount
count of messages.

Installation and Administration Guide

BroadVision, Inc.

72

Chapter 5 Server configuration
Configuring visitor notifications

Job directories

The job directories are created under msg_not_completed limb, and get moved to
msg_completed and msg_failed limbs upon completion of delivery, except messages generated
for a “web” alert [see “sched_srv” on page 75]. They are placed in the bv_web_alert directory, which
is always under msg_not_completed limb. These are processed by the schedule server and remain
in the directory when ﬁnished. As such, the messages and the directory are never moved.

Maintenance

When the schedule server runs, it creates the job directories named either
bv_msg_<oid>_<run-id> (for messages) or bv_alert_<oid>_<run-id> (for alerts). The oid
is the ID of the job, and run-id is a unique ID for the job run. An example is bv_msg_6642_121.

The names of the directories for each run are inserted into the BV_MSGSTAT or BV_ALERTSTAT
tables. If a run did not generate any message, then the directory is removed from the ﬁle system, and
the entry in the table is left empty.

The next section describes the message generating scripts. For information about the generated
messages, see “Messages” on page 73.

When you have many dynamic messages, you can expect them to require a lot of disk space. The
amount of space required is directly dependent on the count of messages to be generated.
Additionally, messages that could not be delivered are placed in directories under the msg_failed
limb, and if bv_schedule_keep_messages is “yes”, messages that were sent are also kept (in the
msg_completed limb). Periodically these directories must be cleaned — possibly after archiving
the messages in them.

The “web” delivery server always writes its ﬁles to the bv_web_alert directory. Periodically you
should remove the ﬁles from the sent_success and sent_failed subdirectories. However,
never remove bv_web_alert from the msg_not_completed limb.

When jobs terminate prematurely — due to a server crash or forced shutdown, for example — the
corresponding directories that have been processed completely for a job are moved to the
sent_success or sent_failed directory. The message directory that is being processed during
the crash usually contains both completed and uncompleted messages after the crash. If you leave
all of the directories intact, some visitors may receive duplicate messages when the system is
restarted. If you move or remove any directories, some visitors may not receive the message at all. It
is safest to not move directories after a crash.

Message backups To make a backup of the messages in the bv_schedule_msg_dir tree, ﬁrst shutdown the

Notiﬁcation servers to ensure that ﬁles do not change during the backup. You can stop them by
following the instructions for shutting down a site as described in “Backing up your site” on
page 141, or you can shutdown the Notiﬁcation servers only, make the backup, and then restart
them. To do that:

To shutdown just the Notiﬁcations servers, stop the sched_poll_d server and it will stop the others
when they complete their jobs:

% $BV1TO1/bin/bvconf shutdownshutdown sched_poll_d

Wait for bvconf to announce that it is done before making the backups. See “shutdown” on page 181
for details about stopping speciﬁc servers.

To restart them

$BV1TO1/bin/bvconf resart -d

The -d option only starts those processes and daemons that are conﬁgured in bv1to1.conf, but not
already running. [See “restart” on page 181 for details.]

BroadVision, Inc.

Installation and Administration Guide

Message scripts

Chapter 5 Server configuration
Configuring visitor notifications

73

The message is generated by a JavaScript script that is able to retrieve information from each
visitor’s proﬁle, and include that information in the message. As an alternative, the message can be
static and not have to be generated for each visitor in the community. The scripts are stored in the
bv_schedule_script_root directory, which by default is $BV1TO1_VAR/msg_scripts/.

bv_schedule_script_root=$getenv(BV1TO1_VAR) + "/msg_scripts/"

This directory must contain the sched_header.jsp file. Copy this file from the
$BV1TO1/lib directory into the bv_schedule_script_root directory. Modify this file for
custom delivery types.

Alternately, scripts are stored in the SCRIPT_TXT column of the BV_MSGSCRIPT table. The actual
location — in ﬁle or in the table — is deﬁned by the SCRIPT_FORM column in the same table.

If the message generating script is stored in a database column, the message size is be limited by
the size of the field in the DBMS, typically about 2,000 characters. For best results, store the
messages as files.

The One-To-One Command Center user can create and edit the script. If the message is stored as a
ﬁle, you need to tell the One-To-One Command Center where to locate the ﬁle, relative to the
machine running the One-To-One Command Center. To do that, deﬁne the Windows-relative path
to the scripts directory with the bv_dcc_schedule_root parameter. For example:

bv_dcc_schedule_root="\\server\bv1to1_var_directory\msg_scripts\"

Similar to the application scripts, the message scripts can have their own, unique components. The
message generator that runs the scripts looks for the components in the bv_js_library_dir
directory, which by default is $BV1TO1/lib/components/.

bv_js_library_dir=$getenv(BV1TO1) + "/lib/components"

Additionally, the message generator can run some scripts when it launches. Such scripts usually
load common library functions that are used by many scripts. When the generator starts, it runs all
of the scripts in the bv_schedule_startup_root directory before running any message
generation scripts. This location is not deﬁned by default.

bv_schedule_startup_root=""

The next section describes the generated messages.

Messages

The script generates the messages. For alerts, the messages are added to the visitor’s proﬁle in the
BV_ALERT_INBOX table. Visitors have the option to indicate whether or not they want to receive
messages by setting the WANT_MESSAGE ﬂag in the BV_USER_PROFILE table. If your site is using
this feature, you should turn on the bv_check_want_message_attr parameter to cause the
message generator to check each visitor’s preference before generating the visitor’s message.

bv_check_want_message_attr="1"

# 1 is check; 0 is don't check

Installation and Administration Guide

BroadVision, Inc.

74

Chapter 5 Server configuration
Configuring visitor notifications

When you are using the e-mail delivery type provided with One-To-One, that generator sends
e-mail to the address deﬁned in the column of the BV_USER_PROFILE table deﬁned by the
bv_email_delivery_addr_attr parameter. By default, it looks in the EMAIL column.

bv_email_delivery_addr_attr="EMAIL"

Some ﬁle systems have a limit to the number of ﬁles that can be stored in a directory. Additionally,
efﬁciency drops when there are many ﬁles to scan and process in a single directory. To increase the
performance and avoid ﬁle-count limitation, deﬁne the count of dynamically generated messages to
store with the bv_schedule_dynamic_msgcount parameter, and deﬁne the count of static
messages with bv_schedule_static_msgcount.

bv_schedule_dynamic_msgcount="2000"
bv_schedule_static_msgcount="2000"

# Dynamic msgs per directory
# Addresses per list

These settings affect the granularity of job division among parallel batch servers. When you are
using batch servers, each processes its own directory (for personalized message) or address-ﬁle (for
static messages). If a job will send less messages than deﬁned by the message count above, it will be
processed by one server and will not beneﬁt from parallel processing.

After the system has successfully processed a message, it can leave it on disc or delete it. By default,
the system keeps the sent message ﬁles for your records. You can change this behavior by setting the
bv_schedule_keep_messages ﬂag to zero:

bv_schedule_keep_messages="1"

# 1 keeps sent msgs; 0 deletes

Processes and daemons

There are four processes and daemons that handle visitor notiﬁcation processing;

l The schedule poller (sched_poll_d)

l The schedule server (sched_srv)

l The delivery servers (such as deliv_smtp_d)

l The delivery completion server (deliv_comp_d)

sched_poll_d

The schedule poller scans the BV_ALERTSCHED and BV_MSGSCHED tables to determine when a
notiﬁcation must be run. When it ﬁnds one that needs to be run, it notiﬁes the schedule server
(sched_srv). A site may have only one schedule poller.

The schedule poller takes these parameters:

Parameter

shutdown

delay

Description

Command used to shutdown the process. It should be a variant of bvkill.

How long (in seconds) after the poller is launched before it should start polling. A delay
is important if the message script relies on other servers or populated caches. The
delay allows the rest of the system to be ready to receive requests from the script.

sleep

How long to wait (in seconds) between polls.

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Configuring visitor notifications

75

Here is an example of a sched_poll_d deﬁnition:

daemon sched_poll_d {

parameter
shutdown="bvkill -w 2 USR1"
delay="600"
sleep="120"

}

# Shutdown command
# Start 10 minutes after launch
# Poll after 120 seconds

The schedule poller issues jobs to the schedule servers, of which there can be several “batch”
schedule servers. During a normal system shutdown (via bvconf shutdown), the schedule poller
waits for all the batch servers currently processing a job to complete their jobs before it shuts down.
This ensures that when a batch server is subsequently shutdown, it is idle. However, if you kill the
server, or if you issues a hard shutdown (such as with bvconf shutdown -f), the poller dies and
does not wait for the schedulers to ﬁnish their jobs. For more information about how shutdown
affects the notiﬁcation servers, see “sched_srv” on page 75 and “deliv_smtp_d” on page 76.

sched_srv

The schedule server runs the script that generates the messages. The messages can be dynamic
(personalized) or static (everyone gets the same message).

Parameter

Description

batch_id

Uniquely, and sequentially identiﬁes a batch server.

server_type

Identiﬁes the type of server as:

web

batch

Handles small jobs that need to be processed quickly because a person is
waiting for the response, such as a One-To-One Command Center user
doing a test or a visitor choosing a “show me the results now” action. You
can have multiple of these type of servers.

Handles jobs that have been set to run in the background at a speciﬁc
time. Each job is assigned to one, and only one, batch server. You can
have multiple of these servers to process multiple simultaneous jobs.
Each server deﬁnition must have a batch_id that identiﬁes the server
from the other batch servers.

parallel

An additional server that runs in parallel with a batch server processing
the same job that the batch server is processing.

Web server

Here is an example of a web server deﬁnition:

process sched_srv {

parameter

server_type="web"

# web scheduler

}

You can have more than one web server, but unless you expect a lot of fast, single-response
notiﬁcations, you should not need to conﬁgure more than a few.

Batch server

The number of batch type servers that you conﬁgure is largely dependent on the count of jobs
scheduled in the site. When the message is static (not personalized) the server generates address
lists that identify everyone that will receive the message. When the message is dynamic
(personalized) the server generates one message for each recipient. In either case, the servers
distribute the work between the batch and parallel servers.

Installation and Administration Guide

BroadVision, Inc.

76

Chapter 5 Server configuration
Configuring visitor notifications

When a job starts, the work is assigned to a batch server. Further, each batch server can have
parallel servers that work on the same job. For example, if there are 12,000 addresses to process,
and 3 parallel servers, each of the 4 servers (1 batch + 3 parallel) processes 3,000 addresses.
You deﬁne the count of parallel servers with the bv_schedule_parallel_count parameter,
and then must deﬁne that many parallel servers for each batch server. For example:

bv_schedule_parallel_count=2

# 2 for each batch server

process sched_srv {

parameter

server_type="batch"
batch_id="1"

# batch scheduler
# ID of this scheduler

}

process sched_srv {

parameter

server_type="parallel"

# 1st parallel scheduler

}

process sched_srv {

parameter

server_type="parallel"

# 2nd parallel scheduler

}

Further, if your site needs to process large jobs simultaneously, you can deﬁne additional batch
servers, just assign a new batch_id to each. The IDs must start with “1” and be numbered
sequentially from there. If you intend to use parallel servers, you must deﬁne
bv_schedule_parallel_count count of parallel servers for each batch server. Then, the
total count of servers is:

(bv_schedule_parallel_count + 1) * batch servers

If you deﬁne fewer parallel servers than required, bvconf will write an error to the log ﬁle
complaining about this. If you deﬁne more than are required, the extras will not be used.

Shutdown issues During a normal system shutdown (via bvconf shutdown), the schedule servers ﬁnish processing
their current job before they shutdown. If you kill the schedule or poller server, or if you issue a hard
shutdown (such as with bvconf shutdown -f), the schedule servers do not ﬁnish their jobs.
Subsequently, when you restart the system, the unﬁnished job is restarted from the beginning,
which can cause multiple messages to be sent to the same recipients.

deliv_smtp_d

This is the delivery server for e-mail type messages. If your site develops other types of delivery
servers, such as fax or pager, you will need to conﬁgure them similar to these directions.

Each server requires three parameter deﬁnitions:

Parameter

Description

delay

id

Seconds to wait after being launched before starting operation.

Uniquely, and sequentially identiﬁes a delivery server.

msg_count

How many messages to send at a time.

msg_delay

Seconds to wait after sending msg_count messages before sending the next set.
Adjust this delay to match the speed that your mail server can send messages.

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Configuring visitor notifications

77

Parameter

Description

ofﬂine

Enables (0) or disables (1) e-mail deliveries. The e-mail delivery server should be
disabled if it is not being used.

shutdown

Command used to shutdown the process. It should be a variant of bvkill.

sleep

Seconds to wait between polls to see if there are messages to deliver.

When you use the deliv_smtp_d server, you must ﬁrst deﬁne the outgoing e-mail server host, as
speciﬁed by the bv_email_host parameter. For example, if the host name is “outbox”:

bv_email_host="outbox"

You can have one or more delivery servers. Deﬁne additional servers when you ﬁnd that the
existing ones cannot keep up with the schedule servers. If you ﬁnd that delivery servers are often
idle when processing messages, you can reduce the count of servers. [See “Monitoring server
statistics” on page 145 for information about watching for idle servers.]

To tell the system how many deliv_smtp_d servers to look for, deﬁne the count with the
bv_email_delivery_server_count parameter. Then deﬁne enough servers to match the
count, and assign an ID to each: the ﬁrst ID must be 1, and each of the rest numbered sequentially.

bv_email_delivery_server_count="3"

daemon deliv_smtp_d {

parameter

shutdown="bvkill -w 2 USR1"
id="1"
delay="600"
sleep="120"
msg_delay="30"
msg_count="10"
offline=0

# Shutdown command
# 1st delivery server
# Seconds to pause after launch.
# Poll after 120 seconds
# Seconds to wait after msg_count
# Messages to send without waiting.
# Enable e-maul delivery

}
daemon deliv_smtp_d {

parameter

shutdown="bvkill -w 2 USR1"
id="2"
delay="600"
sleep="120"
msg_delay="30"
msg_count="10"
offline=0

# Shutdown command
# 2nd delivery server
# Seconds to pause after launch.
# Poll after 120 seconds
# Seconds to wait after msg_count
# Messages to send without waiting.
# Enable e-maul delivery

}
daemon deliv_smtp_d {

parameter

shutdown="bvkill -w 2 USR1"
id="3"
delay="600"
sleep="120"
msg_delay="30"
msg_count="10"
offline=0

# Shutdown command
# 3rd delivery server
# Seconds to pause after launch.
# Poll after 120 seconds
# Seconds to wait after msg_count
# Messages to send without waiting.
# Enable e-maul delivery

}

If bv_email_delivery_server_count value is greater than the count of delivery servers,
some messages will not be sent.

Installation and Administration Guide

BroadVision, Inc.

78

Chapter 5 Server configuration
Defining session profile terms

Depending on the count of messages you are sending, the speed of your Internet connection, and
the performance of your SMTP e-mail transporter, you will need to adjust the delay of the
msg_delay parameter. If the mail is piling up waiting to go out, increase the delay. You should start
with a conservative delay and decrease the wait until you ﬁnd a level that matches the speed the
your mail handler is comfortable with. If the handler is on a dedicated machine with its own T3
connection, you can push considerably more mail than if the server is on a T1 line and doing double
duty handling your normal business correspondence.

Shutdown issues

The e-mail delivery server processes a directory of message ﬁles at a time (or processes a single
address-ﬁle at a time). During a normal system shutdown (via bvconf shutdown), it completes the
delivery processing for the directory or ﬁle before shutting down. If you kill the schedule or delivery
server, or if you issue a hard shutdown (such as with bvconf shutdown -f), the delivery servers
do not ﬁnish their jobs. Subsequently, when you restart the system, the unﬁnished job is restarted
from the beginning, which can cause multiple messages to be sent to the same recipients.

deliv_comp_d

The delivery completion server scans the job directories under the msg_not_completed limb
looking for the gen_complete and gen_failed ﬁles. Depending on the setting of the
bv_schedule_keep_messages parameter:

l If keep messages is 1 (yes), it then moves the message ﬁles from the msg_not_completed limb

into either the msg_completed or msg_failed limbs.

l Otherwise (do not keep messages), it removes the directory from the ﬁle system.

The server then updates the BV_MSGSTAT or BV_ALERTSTAT tables with the statistics about the job.

Parameter

shutdown

sleep

Description

Command used to shutdown the process. It should be a variant of bvkill.

How long to wait (in seconds) between scans.

Here is an example of a deliv_comp_d deﬁnition:

daemon deliv_comp_d {

parameter
shutdown="bvkill -w 2 USR1"
sleep="300"

}

# Shutdown command
# Scan after 300 seconds

A site may have only one delivery completion server.

Defining session profile terms

The BroadVision One-To-One Command Center uses session proﬁle terms to track a visitor’s
moment-to-moment events. Some events are pre-deﬁned and are always available. However, the
Command Center business manager might want additional, custom terms for use in targeting rules.
You deﬁne those terms in the $BV1TO1_VAR/etc/session_terms ﬁle.

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Defining session profile terms

79

When you start One-To-One, bvconf looks for session_terms in $BV1TO1_VAR/etc/. If it
doesn’t ﬁnd it there, it looks for $BV1TO1/lib/session_terms.default, which it then copies
to the etc directory and renames appropriately.

The Content Database service loads the terms from session_terms when it starts up. If you
change the terms in the file, you will need to shutdown and restart the content database
accessor (cntdb). For example:

% bvconf shutdown cndtb
% bvconf restart cndtb

The session_terms ﬁle contains all of the terms for the site, but each term is associated with a
single service only. The ﬁle consists of rows (records) of ASCII text; one term per line, and
terminated with a newline. The syntax for a record is:

serviceName,termName,friendlyName,typeName[,comment]

serviceName

The name of the service that the term belongs to. Use “*” for predeﬁned terms.

termName

The unique name of the term.

friendlyName

typeName

The name that appears to Command Center users. It is a string terminated by a
comma, and without embedded commas.

The name of the type of this session proﬁle term. It should either be “LONG”, or the
name of some subtype of long.

comment

An optional comment that doesn’t appear outside of the ﬁle.

Following is a simple example of the ﬁle:

BestBuyClothing,SportsInterest,Sports Interest,LONG,This term …
BestBuyClothing,GardenInterest,Garden Interest,LONG
SuperDuperBooks,MYSTERY,Mysteries Bought,LONG,How many mystery …
SuperDuperBooks,BIOGRAPHY,Biographies Bought,LONG,How many …
SuperDuperBooks,SCIFI,Saw Science Fiction,LONG,set if user …

Predeﬁned terms You can also assign friendly names to the predeﬁned terms. To do that, use “*” for the serviceName

setting. For example:

*,Bought,Purchased,
*,Chose,Put in basket,
*,Selected,Asked for information
*,Saw,Espied,

Term limit

The default maximum count of custom session terms is 16 per site. You can change this limit by
adding the user_session_terms global setting to the bv1to1.conf conﬁguration ﬁle. For
example, to change the limit to 32, add the following to the site section of bv1to1.conf:

user_session_terms="32"

See “Site conﬁguration” on page 166 for information about setting global (site level) settings.

Installation and Administration Guide

BroadVision, Inc.

80

Chapter 5 Server configuration
Configuring observation logging

Configuring observation logging

When observation logging is on, One-To-One generates log ﬁles that contain raw data that describe
the observations. To turn observation logging on, assign "1" to the observation_flag setting in
the bv1to1.conf conﬁguration ﬁle.

observation_flag="1"

# 1 is on, 0 is off

To turn it off, assign "0" as the value.

The Interaction Manager collects observation information and caches the data in a large buffer.
When the buffer is full, or after a speciﬁed period of time, the Interaction Manager writes the data to
the log ﬁle or ﬁles on disk. By default, the Interaction Manager waits ﬁve minutes before ﬂushing
the cache. You can change the period by specifying the time in minutes to the
observation_flush_time setting in the bv1to1.conf conﬁguration ﬁle.

observation_flush_time="5"

# Flush every 5 minutes

If you are testing observations, you might not see them on disk until you have made several
thousand observations. Flush the buffer by shutting down the Interaction Manager or waiting
observation_flush_time minutes.

Observation log
ﬁles

One-To-One writes observation log ﬁles, by default, to
$BV1TO1_VAR/logs/$BV1TO1_ROOT_HOST/bvobs.out.YYYYMMDD — where YYYYMMDD is the
date the observations were generated. You can change the ﬁlename in the .bvlog.conf ﬁle.
One-To-One creates a new ﬁle when the Interaction Manager ﬂushes its cache of observations, and
one of the events occurred on a new day. When that happens, One-To-One writes the observations to
both the new and old ﬁle — according to the date of the event — until there are no more events from
the old date.

To use observation data in reports, load the raw data from the log ﬁles into the Observation
database, and then aggregate the data into smaller, more manageable tables. See the Database
Administrator’s Guide for details.

Observation error
log ﬁles

Observation errors, if any, are written to the log ﬁle bvlog.out.YYYYMMDD in the
$BV1TO1_VAR/logs/$BV_ROOT_HOST directory. You can change the name and the directory of
the error log ﬁles by changing the speciﬁcation in the logging conﬁguration ﬁle:
$BV1TO1_VAR/etc/.bvlog.conf (note the leading period in the ﬁlename). Edit this text ﬁle and
near the bottom of the ﬁle add a line that begins with “12”, like the following:

12

0:5

/tmp/bvlog.%

RAW

// Log observ. errors to bvlog.YYMMDD

This setting tells One-To-One to generate ﬁlenames in the format bvlog.YYYYMMDD to the /tmp
directory. If you don’t specify a directory, the ﬁles go to the log ﬁle directory.

For more information about .bvlog.conf, see “.bvlog.conf” on page 184.

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Configuring the Matching Agent

81

Configuring the Matching Agent

The Matching system ﬁnds content for a visitor by comparing the visitor’s proﬁle attributes to
similar information in the Content database. To ﬁnd the “best” content for a visitor, the system uses
a Matching Agent. A Matching Agent compares a visitor’s preferences to each content item’s ratings
(taxonomy), and then picks the content that best meets the preferences. The more preferences that
the matching agent can use, the better job it can do ﬁnding desired content.

Matching Agent

Best content

Content
ratings

Visitor
profile

Content
database

For a more complete description of the Matching Agent and the effects of the configuration
settings described in the following sections, see Matching Agent, a supplemental on-line
document.

Content rating values

Matching rating values are stored in the attributes database; visitor proﬁle ratings are stored in the
BV_PROFILE_TAXON, and Content ratings are stored in the individual Content tables, such as the
BV_DISCUSSION and BV_PRODUCT tables Discussion groups and Products, respectively.

Each matching attribute is a character ﬁeld that contains the rating for each topic that the attribute
ranks. Each topic rating constitutes a matching ﬁeld. For example, if your site ranks movies, you
could have a MOVIE_TYPE attribute that might track the relative amount of action, romance, or
science ﬁction in each movie. The MOVIE_TYPE attribute would then contain nine numeric
characters, three characters for each of the matching ﬁelds. If the rating range is 0 to 20, the
MOVIE_TYPE attribute for a content item might contain “020006000” to indicate a high amount of
action, a medium amount of romance, and no amount of science ﬁction.

Attribute

MOVIE_TYPE

Value

020006000

MOVIE_TYPE

Action
Romance
Science Fiction

0 to 20
20
6
0

Correspondingly, the visitor proﬁle might contain “020006002” to indicate high, medium, and low
interest in the three movie categories.

You can track up to 85 ratings (matching ﬁelds) for any attribute, that is, the attribute value can hold
up to 255 (or 85 * 3) characters. Note that a matching attribute must have at least one matching ﬁeld.

Installation and Administration Guide

BroadVision, Inc.

82

Chapter 5 Server configuration
Configuring the Matching Agent

Rating ranges

The range of values that your site accepts is speciﬁed by the taxon_range_upper and
taxon_range_lower settings in the bv1to1.conf conﬁguration ﬁle. The default settings are -5
to 5:

taxon_range_upper="5"
taxon_range_lower="-5"

# Must be a positive integer
# Must be a negative integer or zero

When you use negative values in the range, One-To-One maps them to all positive values by adding
the absolute value of the low range setting to all range speciﬁcations. In this way, all matching
attribute values are stored as positive integers but maintain their relative value. When One-To-One
retrieves the matching attribute values, it maps them back to their original positive and negative
integers. In the following example, the low range value is -5. Since,
maps to “0” in the database, -2 maps to “3”, and +5 maps to “10”.

, the low range

0=

5+

5–

Attribute

MOVIE_TYPE

Value

010003000

MOVIE_TYPE

Action
Romance
Science Fiction

-5 to 5
5
-2
-5

The maximum allowable range is -499 to +500, or 000 to 999.

Your Web site development team can also deﬁne a matching weight for each matching attribute
Matching attributes cause the Matching Agent to favor certain matching attributes over others. A
matching weight is an integer assigned to a single attribute.

Scoring

To present the best possible content, the Matching Agent performs a simple calculation to score each
content item. The higher the score, the greater the likelihood that the visitor will prefer the content.
You can set the Matching Agent to use one of two possible calculations depending on the needs of
your site.

Default algorithm For a single attribute, the Matching Agent determines the best content by following a simple

algorithm:

Profile_rating * Content_rating * weighting_factor = rank

The higher the rank, the greater the likelihood that the visitor will desire the content.

For multiple attributes, the formula is more complex. For details, see Matching Agent, a
supplemental on-line document.

Optimized binary
algorithm

Alternatively, you can set the Matching Agent to use the optimized binary algorithm. This algorithm
has the effect of both increasing the matching speed and reducing the scoring value for each content
item.

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Configuring the Matching Agent

83

The optimized binary algorithm checks to see if the content rating is non-zero. If the rating is zero,
the Matching Agent leaves that matching ﬁeld out of the calculation. If the value is non-zero, the
algorithm calculates the score. Speciﬁcally, for every attribute, sum the proﬁle ratings whose
corresponding content ratings are non-zero, then multiply that sum by the attribute weight, then
add the weighted sums together.

For a single attribute using the optimized method, the Matching Agent determines the best content
by following this algorithm:

Profile_rating * weighting_factor = rank

Again, for multiple attributes, the formula is a lot more complex. For details, see Matching
Agent, a supplemental on-line document.

Specifying the
algorithm

The two algorithms require that you have the same matching attributes in both the visitor proﬁle
and content tables. However, they place different requirements on the range of values you can use in
the content tables. The default algorithm can use the full range of values in the content tables, but
the optimized algorithm cannot. The optimized binary algorithm requires that the values for the
matching attributes in the content tables be either zero (0) or one (1) only. Any other values, including
negative values, will result in that matching ﬁeld being included in the calculation of the score.

To indicate which algorithm your site uses, in the bv1to1.conf conﬁguration ﬁle, set the
taxon_use_binary_val_for_cnt value.

taxon_use_binary_val_for_cnt="0"

# 1 is optimized; 0 uses content

Both algorithms require that you have the same matching attributes in both the visitor proﬁle and
content tables. However, for the optimized algorithm, the values in the content tables should be 1
for Yes and -1 for No. This is because a zero median creates a natural “don’t care” state, and
negative numbers cancel out positives more than zeroes do. For example, -5 x 4 = -20,
while 0 x 4 = 0. In the same fashion negative numbers enforce other negative numbers more than
do zeroes.

Rankings and cutoffs

The highest possible rank that a match can have is equal to the count of attributes compared, times
the highest value each attribute can have (its upper range), times the weighting factor.

(attribute count) * (highest value)2 * weight = maximum score

This value, the maximum score, can be a large number. For example, if there are three ratings, each of
which can have a high value of 5, and the weighting factor is 10, then the maximum possible score is
750.

If the visitor, however, rates each of the attributes low or “undesirable”, say with values of 0, 1, and
1, the ranking score for a match would be 60 (3*2*10). This is a 8% likelihood (60/750) that the
visitor will like the content.

One of the visitor proﬁle attributes is a cutoff value ( MATCHING_PERCENT_CUTOFF) that speciﬁes a
minimum percentage likelihood match that the visitor is willing to consider. The business manager
may also specify the cutoff in the matching rule as speciﬁed by the One-To-One Command Center.
Both of which are optional features. However, when the cutoff is speciﬁed, the Matching System
discards all matches that fall below the cutoff value. So, from the example above, had the cutoff been
20%, the 12.5% match would have been discarded. The default cutoff is zero percent.

Installation and Administration Guide

BroadVision, Inc.

84

Chapter 5 Server configuration
Configuring the Matching Agent

When cutoffs values are high, it is common to have most or all matches discarded. This can happen
when:

l visitors specify low values for most ratings

l visitors don’t specify all rating values, and the default values are zero

l matching rules include many attributes, which in turn create very large maximum scores

To improve the likelihood of ﬁnding matches when cutoffs are in effect, you can override the
maximum score calculation and specify a ﬁxed value with the taxon_max_score setting in the
bv1to1.conf conﬁguration ﬁle. This setting speciﬁes the maximum score that the Matching Agent
uses in calculating the percentage of match between a content item and the preferences speciﬁed in
the visitor’s proﬁle.

score / maximum score = percentage match

For example, the following line speciﬁes 500 as the maximum score for the site:

taxon_max_score="500"

With a maximum score of 500, the percentage matches for the previous example change
signiﬁcantly, causing Terminator to be displayed even with a cutoff of 60 percent.

Percentage of match for Terminator

Percentage of match for “Bridges”

400/500=

105/500=

80%

21%

The default setting is “0” which tells the matching system to use a calculated maximum score for
each comparison. Changing the default setting to any other positive value, tells the Matching Agent
to use that value as the maximum score instead of the calculated maximum score. The calculated
maximum score is different for the two algorithms.

Content order

A request for matching content frequently retrieves a list of multiple content items. By default, the
Matching System presents the content item with the highest percentage of match ﬁrst with the rest
listed in descending order. The Matching System does this for each matching rule, with sorted
content from subsequent rules being appended to the sorted content from the previous rule. You can
change the sort order to ascending—lowest percentage of match to highest percent of match—by
changing the taxon_sort_order setting in the bv1to1.conf conﬁguration ﬁle.

taxon_sort_order="DESC"  # DESC is descending; ASC ascending

BroadVision, Inc.

Installation and Administration Guide

Adding an input argument to the Matching Agent

Chapter 5 Server configuration
Adding an input argument to the Matching Agent

85

One-To-One supplies two versions of the Matching Agent. One version displays an input argument
ﬁeld in the Matching Rule Action dialog and the other version does not. This argument ﬁeld allows
you to change the default Matching Agent cutoff.

The Matching Agent cutoff is a percentage value the Matching system uses to determine whether to
display certain content. Content that has a match percentage below the cutoff is not displayed to the
visitor.

You can use this argument ﬁeld to change the default cutoff percentage for the Matching Agent by
entering a number between zero (the default) and 100. In this way you can change the default cutoff
percentage for each Matching Rule that uses the Matching Agent.

To add the input argument to the Matching Agent do the following:

1. Edit the following ﬁle:

$BV1TO1/bin/scripts/match_func.sql

Near the top of this ﬁle are two segments of code, one labelled version A and one labelled
version B. In the default condition for this ﬁle, version B is commented out. You need to
comment-out version A and uncomment version B as shown below:

/*

* version A: Matching Agent without input argument. This is default.
*
*insert into BV_TARGET_FUNC values
*('bv_action_func_taxonomy', 1, 2, 'Matching Agent', 0, 'LONG',
'Compare visitor preferences to your content ratings to pick
content based on the resulting score.', 0, '', 2, 1)

*go
*/

/*

* version B: Matching Agent with input argument.
*/

insert into BV_TARGET_FUNC values
('bv_action_func_taxonomy', 1, 2, 'Matching Agent', 0, 'LONG',

'Compare visitor preferences to your content ratings to pick

content based on the resulting score. Enter the cutoff value in
the range 0-100 as a setting if you want to override the
default value of 0.', 1, '0', 2, 1)

go

2. Use apply_sql to make version B the active Matching Agent:

% $BV1TO1/bin/scripts/apply_sql match_func.sql

Installation and Administration Guide

BroadVision, Inc.

86

Chapter 5 Server configuration
Setting matching and pricing rule evaluation time

Setting matching and pricing rule evaluation time

Matching and pricing rules can include a time period for which they are valid. To test a rule that has
a time constraint, you can run the system in a test mode that causes the system to believe that the
“current” time is a value you specify.

To place the system in this test mode:

1. Create a text ﬁle named rule_eval_time, and place it in the $BV1TO1_VAR/etc/ directory.
For your convenience, there is a sample of this ﬁle in the $BV1TO1/lib/ directory; copy that
ﬁle if you so desire.

2. Edit the rule_eval_time ﬁle and specify the date and time you want to become the testing

time. The format is as follow:

# datetime format: MM/DD/YYYY HH:MM:SS
1/6/2003 12:00:00

3. Turn testing mode on by stopping and then restarting the Interaction Manager. If you have

multiple Interaction Managers, restart all of them. See “Shutting down your site” on page 138
and “Restarting your site” on page 139 for details.

% $BV1TO1/bin/imgr_conf -a stop
% $BV1TO1/bin/imgr_conf

When Interaction Manager detects the ﬁle it switches into testing mode, and continues to check the
ﬁle to determine the test time. In this way, you can change the value in the ﬁle and the Interaction
Manager will change its test time to the new setting. Whenever it detects a time change, the
Interaction Manager writes a message to its log ﬁle to indicate the state change.

To return to normal, production mode, remove the ﬁle from the directory and restart the Interaction
Manager.

Using the Verity search engine

The One-To-One search feature uses the Verity Search’97 engine to provide full-text searching
One-To-One content and of external ﬁles. The search retrieves results with relevance-ranked scores
and the results can be ordered by the score or by any of the ﬁelds deﬁned by the conﬁguration.

The Verity search engine requires an additional license for use; it is not part of the standard
BroadVision One-To-One Enterprise license.

To use the search engine, you need to:

1. Conﬁgure the bv1to1.conf conﬁguration ﬁle.

2. Identify what database attributes and ﬁles can be searched.

3. Create a search collection by running the indexer utility.

4. Keep the collection up to date as content changes.

BroadVision, Inc.

Installation and Administration Guide

The One-To-One installation procedure does not install the Verity software by default. During the
installation, you have to tell the installation script to perform a non-default install, and then choose
to install the Verity software. If Verity is not installed in your system and you have obtained a license
for it, re-run the script and install just the Verity package.

Chapter 5 Server configuration
Using the Verity search engine

87

Conﬁguring One-To-One for Verity

The Verity executables directory must be included in the One-To-One ﬁle-search path. By default,
the ﬁles are install in $BV1TO1/verity/common, and is included in the $BV_PATH deﬁnition.

# Search paths
BV_PATH=$getenv(BV1TO1) + "/bin"

+ ":" + $getenv(BV1TO1) + "/orbix/bin"
+ ":" + $getenv(BV_DB_BASE) + "/bin"
+ ":" + $getenv(BV1TO1) + "/verity/common"

If you locate it elsewhere, update this path and re-run bvconf execute to effect the change.

Additionally, by default bvconf execute will create a $BV1TO1_VAR/collection directory.
This will contain conﬁguration information speciﬁc to your site, and it will contain the index of
words in your system. As such, be sure that this directory is on a sufﬁciently large disk drive.

Identifying what to index

The search feature can locate words in the One-To-One content tables, or in external ﬁles using
either full-text or ﬁeld-search features.

l Full-text search looks in the entire document or identiﬁed database columns for the desired text.
To look in a database column, the attribute must be deﬁned as either TEXT or STRING. To
search any other type requires a ﬁeld-search.

l Field-search looks for the text in format-speciﬁc ﬁelds. For example, when searching an external
ﬁle of a type that Verity supports, such as PDF, you can search for the document’s creation date
because that information is stored in a known location within the PDF ﬁle.

A ﬁeld-search ﬁeld can also be an attribute of the One-To-One content database.

A ﬁeld-search is faster than a full-text search because it limits the search to a smaller set of data, and
it is better at identifying what the searcher is looking for. For example, if you perform a full-text
search for a speciﬁc date, the search will return all documents that have that date in them. But a
ﬁeld-search can limit the return list to just those documents that were created on the speciﬁed date.

Field deﬁnitions

To perform a ﬁeld-search, a visitor speciﬁes the ﬁeld and the desired text, similar to this:

Author <CONTAINS> Jason

Verity is able to perform a ﬁeld search quickly because it builds a table that contains a row for each
document that has been indexed, and each row contains columns that have the ﬁeld-speciﬁc
information. In the example above, Verity searches the Author column in its table of documents.

Installation and Administration Guide

BroadVision, Inc.

88

Chapter 5 Server configuration
Using the Verity search engine

For external ﬁles, Verity needs to know where to look in the ﬁle for the named ﬁeld’s information; in
the example above, Verity needs to know where to locate the “Author” data. It does this through
ﬁlters. Verity provides ﬁlters for many common ﬁle format, such as HTML ﬁles, Microsoft Word
documents, and PDF ﬁles. You can acquire additional ﬁlters from Verity, or write your own. See the
Verity documentation for details about ﬁlters.

To perform ﬁeld-searches on the One-To-One content database, you need to tell the indexer which
One-To-One attributes get mapped to which ﬁelds in the Verity database. The Verity database ﬁelds
(it schema) are deﬁned in style ﬁles. By default, One-To-One provides three sets of style ﬁles:

Location

Description

$BV1TO1/verity/common/style

Default system styles, do notchange these.

$BV1TO1_VAR/collection/style/EDITORIAL

Editorial content speciﬁc styles.

$BV1TO1_VAR/collection/style/PRODUCT

Product content speciﬁc styles.

The One-To-One-speciﬁc ﬁelds are deﬁned in the style.ufl ﬁles in the directories noted above.

Product ﬁelds

OID

Store_Id

Editorial ﬁelds

OID

Store_Id

Creation_Date

Creation_Date

Price

To add additional fields, modify the files according to the specifications in the Verity
documentation. That documentation also discusses how to use other style files to perform such
tasks as soundex searches.

Once the Verity ﬁelds have been deﬁned, you need to provide the mapping from the attributes to the
ﬁelds.

Attribute
mappings ﬁle

An attribute mappings ﬁle tells Verity which One-To-One content columns can be searched. You
create this ﬁle and assign it a name of your choosing, in a location of your choice. There are no
defaults provided with One-To-One.

The ﬁle lists all the searchable attributes for a table, and identiﬁes the type as ﬁeld-search only
(FIELD), full-text search only (TEXT), or both (BOTH). Additionally, for ﬁeld-searches, the ﬁle maps
the attributes to the Verity ﬁeld names. In this example, the ﬁrst column is the attribute, followed by
the type of search allowed on the attribute, and a Verity ﬁeld name — NA stands for “not
applicable”.

OID
ED_NAME
AUTHOR
LAST_MOD_TIME
PUBLISHER
CONTENT_FILE
COMMENTS

FIELD
BOTH
BOTH
FIELD
TEXT
TEXT
TEXT

OID
Title
Author
Date
NA
NA
NA

BroadVision, Inc.

Installation and Administration Guide

External ﬁles

Chapter 5 Server configuration
Using the Verity search engine

89

Note that each row in the content database maps to one row in the Verity table. As such, ﬁelds must
map to one, and only one, attribute.

To perform a full-text search, the attribute’s data type must be either TEXT, STRING, or
FILE_PATH. Otherwise, you have to use field-search.

Later, after generating the collection from the mapping ﬁle above, you can perform a full-text and
ﬁeld-search on the attributes and ﬁelds. For example, the following query ﬁeld-searches the
collection for content items whose LAST_MOD_TIME is later than 1/1/98, and whose AUTHOR
contains “BroadVision”, and it full-text searches for “shopping” in all of the attributes except OID,
and LAST_MOD_TIME:

AND(Date > Jan 1 1998, Author <CONTAINS> BroadVision, shopping)

The detailed query expression syntax can be found in the Verity documentation.

To search an external ﬁle, the ﬁle has to be identiﬁed in an attribute in a content table, and that
attribute must be a FILE_PATH data type. Additionally, the text in the attribute identiﬁes the ﬁle’s
location, relative to the HTTP server’s document root directory. (The document root directory is the
default location where the HTTP server looks for ﬁles.) For example, a URL to a speciﬁc ﬁle might
be http://www.broadvision.com/scores/latest.pdf, but the FILE_PATH attribute value
that locates this ﬁle is “/scores/latest.pdf”.

After the ﬁelds and the content mapping ﬁles have been deﬁned, you can run the indexer to build
the Verity collections.

Some site configurations do not allow the machine that runs the One-To-One servers to access
the file system of the HTTP machine. To make the external files both indexable by indexer, and
locatable by the HTTP server, you need to establish a local directory tree that mirrors the
document root directory tree. All the searchable files and directories in the HTTP document root must
exist in the mirror. For example, while the HTTP document root might be
/opt/local/www/, the local mirror might be /home/webfiles/. Then you would tell the
indexer to use local directory for the -r option, but the file specification in the database
would be “/scores/latest.pdf”, which is relative to both locations.

Some sites also have conﬁgurations with multiple HTTP servers each running on their own ﬁle
system for performance reasons. In those conﬁgurations, the sites typically already have a
means of mirroring or cloning the document root directory across the machines. In this type of
conﬁguration, include a means for letting the indexer see one of the clones.

Creating a search collection

Before the One-To-One search feature can be used, you must create a Verity search collection. A
search collection represents “metadata” for a set of documents, and the collection’s architecture is
optimized for searching. The process of building collections is called indexing, and it is performed
with the indexer tool.

To run the indexer and create the search collection, you need to at least identify the HTTP server’s
document root directory with the -r argument, and should identify the One-To-One service that
owns the content to be indexed. Do that with the -service_name argument. For example, to index
the content that belongs to the MyBank service:

% indexer -service_name MyBank -r /docroot/filepath

If you do not have any external files, you can omit the -r option.

Installation and Administration Guide

BroadVision, Inc.

90

Chapter 5 Server configuration
Using the Verity search engine

The example above indexes the Editorial data for the MyBank service. If you do not identify the
content type with the -content_name option, the indexer defaults to Editorial content. This
example indexes the PRODUCT content, and includes the -f option to use an Attribute mappings
ﬁle speciﬁc to the Product schema:

indexer -service_name MyBank -content_name PRODUCT \

-r /docroot/filepath \
-f $BV1TO1_VAR/mappings/prodMapFile

If you omit the -f argument, the indexer does a full-text index (TEXT) on all the attributes of type
TEXT, STRING, or FILE_PATH in the content table, and you cannot then do a ﬁeld (FIELD) search
on the content.

The indexer uses the $BV1TO1/collection/tmp directory to dump content database into
files that can be indexed, and it uses the directory to create bulk submit files. Do not remove the
contents on this directory while the indexer is running. You can specify a different directory
with the -t option.

Excluding content When you run the indexer, you can use a special argument to exclude the content in speciﬁc

categories from the indexing process. By excluding content items from the indexing process, you
also exclude them as items that can be searched for and retrieved by the Search feature.

To eliminate content items as searchable content, create a ﬁle that contains paths to the content
categories you want to exclude. Enter one line item in the ﬁle for each category path to content that
you don’t want to index. For example, these entries are in a ﬁle named product_excludes.dat:

/Products/Mutual_Funds/Personal_Portfolios
/Products/Mutual_Funds/Bond_Funds/obsolete_bond_funds
/Products/Unclassified

To exclude the items, run the indexer using the -exclude_cat argument:

indexer -service_name MyBank -content_name PRODUCT \
-exclude_cat product_excludes.dat \
-r /docroot/filepath \
-f $BV1TO1_VAR/mappings/prodMapFile -b

There is also a corresponding -include_cat argument that adds instead of excludes.

Indexing
directories

Sometimes a content record points to a directory of documents, such as the HTML ﬁles for a
manual. To index all of the ﬁles in directory, and have them be related to the content record, specify
the -dir_flag option.

indexer -service_name MyBank -content_name MANUALS \
-r /docroot \

-dir_flag

Then, when the indexer encounters an asterisk (*) wildcard for the ﬁlename in a FILE_PATH
attribute (such as /APIRef/*), it indexes all of the ﬁles in that directory.

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Changing the site ID

91

Maintaining up-to-date Verity collections

After content has been modiﬁed, the index needs to be updated to reﬂect the change. The -b option
tells the indexer to completely rebuild the collection. By default, the indexer performs an
incremental update that ﬁnds database content or external ﬁles modiﬁed since the last time the
indexing program was run. However, it does not remove obsolete references from the index. As
such, a search can “ﬁnd” items that no longer exist.

indexer -service_name MyBank -content_name PRODUCT \

-r /home/www/docroot \
-f $BV1TO1_VAR/mappings/prodMapFile -b

Use -b after removing data, and occasionally to build a new, balanced index. Otherwise, omit the
option when you need to add new items to the index.

Changing the site ID

In the database, each One-To-One content item has a ID called an OID (object ID). These values are
unique within a One-To-One installation. If you have multiple installations, such as one for
production and another for development, you will mostly likely have problems copying content
data between them because the OIDs will conﬂict: not be unique.

The bv_site_id setting in the bv1to1.conf conﬁguration ﬁle allows you to assign a site ID to an
installation. That ID then becomes part of the OID and allows you to copy content between the
installations. When you use a site ID, it is applied to all content OID generation, including the
negative OIDs of categories, except for

l user IDs

l user payment type IDs

l account IDs

l store IDs

l order management transaction IDs.

You do not have to use a site ID if you have only one installation, or if you do not copy content data
between sites. By default, this feature is turned off because it limits the maximum count of OIDs
generated per site to around 500 million content items.

Setting a site ID

To assign a site ID to an installation, set bv_site_id to an integer value from 0 to 3, inclusive. (You
can have up to four unique site IDs.)

bv_site_id = 0

# Site 0

The site ID value is assigned to the two most-signiﬁcant bits of the OID. If you have existing data in
one of your sites and later want to turn on the site ID feature, assign zero (0) to that site to not affect
the existing OIDs.

Do not change the bv_site_id setting once you have created content for a site. Doing so can
cause duplicate OIDs if you have multiple sites.

Installation and Administration Guide

BroadVision, Inc.

92

Chapter 5 Server configuration
Running multiple One-To-One servers on one host

When you start One-To-One with the bv_site_id setting in use, bvconf checks for the existence of,
and creates if necessary the $BV1TO1_VAR/bv_site_id ﬁle. Never edit this ﬁle! If you reconﬁgure
your installation to use a different setting, bvconf will terminate with an error. Speciﬁcally, running
bvconf with

l execute -a install_all creates or overwrites the ﬁle. This command also empties the

database so there is no concern about losing IDs; everything will be lost.

l execute creates the ﬁle if it doesn’t exist. If the ﬁle exists, but with a different value than the

setting, bvconf terminates with an error.

l restart checks for the existence of the ﬁle if the setting is deﬁned.

• If there is no ﬁle, bvconf terminates with an error. Run bvconf execute instead to

recognize the change.

• If the ﬁle exists but with a different value from the setting, bvconf terminates with an error.
Change the setting to match the value in the ﬁle and run bvconf execute to recognize the
change.

Running multiple One-To-One servers on one host

You can run multiple instances or multiple versions of One-To-One on a single host, provided that
you conﬁgure them to not collide in key areas. To run multiple instance or versions of One-To-One
on a single host, each installation needs a unique:

l $BV1TO1_VAR directory of conﬁguration speciﬁc ﬁles. See “Files and directories,” below, and

“One-To-One variables” on page 32 for more information.

l $IT_DAEMON_PORT port number for accessing the (ORB). Ideally, each should also have a unique

$IT_DAEMON_BASE to stop servers competing for the same sockets. See “One-To-One
variables” on page 32 for more information.

l Instance name (Windows NT only) deﬁned by the $BV1TO1_INSTANCE variable. This variable
is created by the bvconf execute command’s -i instance_name (Windows NT only)
option. When you use that option, bvconf deﬁnes $BV1TO1_INSTANCE as an export variable
in the Shell start-up scripts in the $BV1TO1_VAR/etc directory. Be sure to “source” a start-up
script before restarting the servers, or starting the Interaction Manager servers. The following
example, creates an instance named test_site, starts and stops the servers, sources the
environment variables, and then restarts the servers. Because the $BV1TO1_VAR deﬁnition has
not changed, the servers pickup the instance name from the $BV1TO1_INSTANCE variable
deﬁned in the schell start-up script.

bvconf execute -i test_site
bvconf shutdown
. $BV1TO1_VAR/etc/bv1to1.conf.sh
bvconf restart

l Database to store installation speciﬁc information. Alternately, each installation must at least use
a different database user account. See “Database variables” on page 33 for more information.

l Script and Page template directories. See “Conﬁguring the Interaction Manager server” on

page 40 for more information.

l Component and dynamic object library directories to contain the components objects speciﬁc to
the site. Each installation has a different shared object library. See “Conﬁguring the Interaction
Manager server” on page 40 for more information.

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Running a multiple-host configuration

93

l Gateway server. Different versions of One-To-One require different CGI server instances. To run
different versions of One-To-One on the same machine, give each CGI gateway a unique name.
See “Conﬁguring the gateway for a standard CGI server” on page 48 for more information.

Additionally:

l Run one Interaction Manager for each One-To-One installation. However, at least one of the
managers must be a named application; you cannot use the default name for more than one
One-To-One installation. See “Running multiple applications on a single CGI host” on page 111
for details.

l The multiple installation may share the same HTTP daemon as long as each application has a
different starting page; the ﬁrst page that the visitor sees. That page will then direct the visitor
into the correct One-To-One application. Alternately, each installation can use its own HTTPd.

Files and
directories

One-To-One stores all of its critical data in the database. Additionally, conﬁguration and writable
ﬁles are stored in the $BV1TO1_VAR directory. The One-To-One system ﬁles are stored in the
$BV1TO1 directory. If you are not familiar with these environment variables and directories, see
“Deﬁning system environment variables” on page 31.

To run multiple instances or versions of One-To-One on one host, such as for separate development
and production systems, install the One-To-One software for each into separate directories, and
have each system access a separate database.

Production
One-To-One

Each system has its own
database and $BV1TO1
and $BV1TO1_VAR
directories and files.

Development
One-To-One

Production
database

$BV1TO1/
$BV1TO1_VAR/

Development
database

$BV1TO1/
$BV1TO1_VAR/

When you install a new One-To-One system, the database and $BV1TO1_VAR directory are both
empty. Both get conﬁgured and populated when you run the bvconf utility to start the system. This
utility gets the site’s conﬁguration information from the bv1to1.conf ﬁle located in the
$BV1TO1_VAR/etc directory. If it doesn’t ﬁnd the ﬁle in that directory, it reads the default
conﬁguration from the bv1to1.conf.default ﬁle in the $BV1TO1/lib directory.

Running a multiple-host configuration

The One-To-One and Interaction Manager servers are designed to run on distributed hosts. All
One-To-One and Interaction Manager servers communicate with each other via CORBA, and many
of them read ﬁles from and write ﬁles to common locations deﬁned by the $BV1TO1 and
$BV1TO1_VAR directories. If all of the hosts can access the common locations, such as with NFS on
UNIX or with UNC on Windows NT, you need do nothing special except possibly to deﬁne in the
bv1to1.conf ﬁle, the host machines and possibly identify the remote shell to use when accessing
those hosts [see Step 3 and Step 4 below for details].

Installation and Administration Guide

BroadVision, Inc.

94

Chapter 5 Server configuration
Running a multiple-host configuration

However, if the servers cannot access the same ﬁle locations, such as because of a ﬁrewall, you must
conﬁgure the system as follows:

1. Install One-To-One in the same location — the $BV1TO1 directory — on each host machine,

such as /opt/bv1to1/ or c:/bv1to1/. The installation process populates this location with
the One-To-One and Interaction Manager executable ﬁles. This location must be the same on each
host. See Chapter 2, “Installation,” for complete instructions.

2. Set $IT_DAEMON_PORT to the same port number on each machine. The CORBA servers on each

machine use the same port number for communicating to the ORB.

3. Deﬁne the hostmgr parameters in bv1to1.conf for each Interaction Manager stand-alone

host. For example:

process hostmgr {parameter host="host1"}

When One-To-One starts on the root host (the machine where you run bvconf), it launches a
CORBA servers on each hostmgr host to allow the Interaction Manager servers to
communicate with the One-To-One servers. You do not need to deﬁne hostmgr for hosts that
are also running One-To-One servers, because they automatically launch the ORB when
One-To-One starts. See the description of the hostmgr parameter on page 171 for details.

4. UNIX: Set the BV_RSH_PATH parameter in bv1to1.conf if you need a different shell tool. The
bvconf utility uses a remote shell to execute commands on remote hosts, including Interaction
Manager hosts. However, for security reasons, some sites do not allow applications to run
remote shells. If you have another utility that performs the remote shell functionality, you can
tell bvconf to use that utility with the BV_RSH_PATH parameter. See “Remote shell” on
page 165 for details.

5. Windows NT: Deﬁne the name for the One-To-One instance on all of the machines in the same
instance; deﬁne the name with the $BV1TO1_INSTANCE variable. This variable is created by
the bvconf execute command’s -i instance_name (Windows NT only) option, which
adds it to the Shell start-up scripts in the $BV1TO1_VAR/etc directory. Always “source” a start-
up script before starting servers.

6. Set the database environment variables on all machines running database accessor servers, and
the Interaction Manager servers. See “Database variables” on page 33 for more information
about setting these variables.

7. Create identical $BV1TO1_VAR locations accessible to each Interaction Manager host. This
location is where the servers get their conﬁguration information, and where the write
observation and log ﬁle data. This location must be the same on each host; for example, if it is
c:/bv1to1_site/, it must be that location on every host.

Whenever you change the site conﬁguration, from the root host:

a. Copy the $BV1TO1_VAR/var/orb directory contents to each distributed host. This

directory contains the Orbix CORBA conﬁguration information.

b. On each distributed host, remove the $BV1TO1_VAR/var/orb/Repository directory.

c. Copy the $BV1TO1_VAR/etc/ directory contents to each distributed host. This directory

contains the site conﬁguration information.

d. If you use the dump_taxon utility, copy the $BV1TO1_VAR/cache/taxon ﬁle to each
distributed host. This ﬁle is the category and matching attributes cache ﬁle that the
Interaction Manager can use for fast matching.

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Running a multiple-site configuration

95

8. Make the log ﬁles directory accessible to all servers. Servers write observation and log message
data to the $BV1TO1_VAR/logs/hostName directory, where hostName is the name of the
server host machine. In a multiple-host conﬁguration environment, accessing $BV1TO1_VAR is
often inefﬁcient.

On Solaris: The logs directory must be visible to the servers, however, there is no requirement
that all servers write to the same ﬁle system. For better performance, some sites conﬁgure this
location to be a symbolic link that writes the information to a local hard disk.

On HP-UX and Windows NT: Instead, deﬁne $BVLOG_DIR in the bv1to1.conf ﬁle to identify
the directory where servers will write the ﬁles on the local host. Then, the ﬁles will be written to
$BVLOG_DIR/logs/hostName. The directory must exist on all host machines before starting the
servers on that machine.

To aggregate observation data, the ﬁles from all hosts must ﬁrst be copied to a central location.
See the Database Administrator’s Guide for details.

9. All machines must use the same login account to launch the One-To-One and Interaction

Manager servers, and that account must not be a root level account.

Later, when you start the servers, start the One-To-One servers on the root host, and then start the
Interaction Manager servers on the remote hosts.

Running a multiple-site configuration

A One-To-One application usually runs on a single site, with all back-end One-To-One servers and
Interaction Manager engines running on machines that are in close proximity. However, it is
possible to run One-To-One in a multiple-site conﬁguration where “related” One-To-One systems are
running in potentially geographically separate sites.

These sites may be alike in the sense that they all run the same set of applications, or they may be
diverse — each site running its own. A like-site conﬁguration usually occurs when the application
must be ceased from geographically diverse locations, or to provide better protection against site
level failure. A diverse-site conﬁguration allows the divisions of a large company more autonomy in
managing their own (sub-)sites.

Issues

In a multiple-site conﬁguration:

l There is one shared database. One-To-One stores application data in a database. For a multiple-
site conﬁguration, you must employ the appropriate database technologies (such as replication)
so that to all sites, there is a single set of consistent One-To-One database tables.

l The database is the only shared data storage. Other than the database, sites do not share any

persistent storage for One-To-One. In particular, $BV1TO1_VAR location is local and exclusive
to each site. Sites also have their own scripts and page templates, as well as HTTP document-
root directories.

l Inter-site CORBA traffic is available. Inter-site CORBA calls are used mainly for operations like

cache ﬂushing. If the applications so partition the data that sites do not step into each other, this
requirement may be waived. (For example, if each site has its own site ID, then content is not

Installation and Administration Guide

BroadVision, Inc.

96

Chapter 5 Server configuration
Running a multiple-site configuration

shared.) If inter-site CORBA trafﬁc is expected, all sites must use the same IT_DAEMON_PORT.
Also, host name resolution in all sites must be consistent so that CORBA object references
remain valid across site boundary.

The name space is the “repository” of CORBA objects. Servers “publish” their CORBA objects by
putting them into the name space. Each site has its own name space; each must have its own
bvconf_srv process.

process bvconf_srv {}

The name space path for each CORBA object installation is deﬁned in the bv1to1.conf
conﬁguration ﬁle. For example, content database accessors are installed using the cntdb_path
parameter.

cntdb_path="CntMgmt/CntDB/cntdb"

Likewise, clients must locate server objects through the name space. They must follow the
convention used by the servers to compute the name space path of the target objects, and they
may not use the _bind() method.

l Sites are not equal. For like-sites, all One-To-One visitor functionality should available in every
site: an application should not be crippled in if a visitor comes in via this instead of that site. But,
Sites may differ signiﬁcantly in terms of their individual conﬁgurations, particularly with
regards to back-end processing like payment settlement, which may be running only in one
designated site.

l The application determines if a multiple-site configuration is possible and reasonable. Two rules of

thumb are:

• If there is partition of application data by site, the sites can operate more independently.

• Stateless and independent front-line servers can more likely be replicated across sites than

back-end daemons.

Server/daemon

Front-line

Back-end

alert_srv

bvconf_srv

cmsdb

cntdb

deliv_comp_d

deliv_smtp_d

extdbacc

genericdb

ofbe_srv

ofdb

om_srv

pmtassign_d

pmthdlr_d

pmtsettle_d

sched_poll_d

sched_srv

Yes

Yes

Yes

Yes

No

No

Yes

Yes

No

Yes

Yes

No

No

No

No

No

No

No

No

Yes

Yes

No

No

Yes

No

No

Yes

Yes

Yes

Yes

Yes (web mode)

Yes (batch/parallel mode)

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Running a multiple-site configuration

97

l Sites may have different configurations. The difference, however, is limited to server and process

conﬁguration and performance related parameters (such as content cache sizes). [See
“Conﬁguring a multiple-site system” on page 97.]

l Only one site may provide background schedule processing. That site must have a single instance
each of sched_poll_d, deliv_comp_d, and sched_srv (the “batch” mode scheduler). Each
site may have multiple instances of “web” mode scheduler (sched_srv) and the e-mail
daemon (deliv_smtp_d).

l Multiple sites may use order management. However, the identically conﬁgured payment

daemons may be on-line in only one site at a time.

l Sites are individually managed in a coordinated manner. There is no tool to centrally manage all
the sites; operators of the sites do their own bvconf execute and shutdown operations. On
the other hand, conﬁguration and operation of the sites must be coordinated.

l Performance is configuration and application dependent. Compared with a single-site setup, a
multi-site conﬁguration has many more variables (such as database replication and WAN
connectivity) that can affect performance.

Conﬁguring a multiple-site system

Site conﬁguration is speciﬁed in the bv1to1.conf conﬁguration ﬁle. Sites may have different
conﬁgurations, however, it is best to have one master ﬁle that all of the site use, especially for like-
site conﬁgurations. The difference between the site conﬁgurations is limited to server and process
conﬁguration, and performance related parameters (such as content cache sizes). Additionally,

l Conﬁguration items with database implication, like the set of services as well as the

default_service and privacy_flag parameters, must be the same across all sites.

l Name space path parameters (such as cntdb_path) must be consistent.

l Client side parameters (such as default_country) may vary.

l Use the site parameter to conﬁgure each site in the master conﬁguration ﬁle.

Site parameter

The bv1to1.conf conﬁguration ﬁle may have multiple site sections in the ﬁle. For example:

define
...
export
...

site eastcoast {

...

}
site westcoast {

...

}

When you have multiple site conﬁgurations, use the -S option of bvconf execute to identify
which site you are starting. For example, to start the West Coast site:

% bvconf execute -S westcoast

Installation and Administration Guide

BroadVision, Inc.

98

Chapter 5 Server configuration
Running a multiple-site configuration

Global
speciﬁcations

For global speciﬁcations, place parameters are the ﬁle-level: before the ﬁrst site deﬁnition. For
example, in this conﬁguration the x parameter has the same deﬁnition in both sites:

define
...
export
...
parameter

x = "y";

site eastcoast {

...

}
site westcoast {

...

}

Each site deﬁnition may also have it’s own export section that overrides global deﬁnitions.

Host override

The -H option has priority over -S. If a server or daemon is assigned to a host not in the -H list, that
server or daemon is not started. For example, consider the following conﬁguration that uses a host
speciﬁcation for the payment handler:

define
...
export
...

site eastcoast {

...
daemon pmtsettle_d {

parameter host = "mars"

...

}
...

}

Running the following bvconf command does not start the pmtsettle_d daemon, even though it
is deﬁned for the site.

% bvconf execute -S eastcoast -H earth,neptune

Updating name space objects across sites

The bvconf ns command with its -g and -p options respectively “get” or “push” from or to the
remote host. Objects in the source context not already in the target are added to the target. For
example, to get the Interaction Manager objects (bvsmgr) from a machine name earth onto the
current machine:

$ bvconf ns -H earth -g bvsmgr

To push from the current machine to earth:

$ bvconf ns -H earth -p bvsmgr

BroadVision, Inc.

Installation and Administration Guide

Chapter 5 Server configuration
Running a multiple-site configuration

99

Note, unlike Interaction Manager namespace objects, cache control objects (BV_CacheControl) are
installed into one naming context. For example, the scheduler cache is deﬁned by
cachecontrol_path in the bv1to1.conf conﬁguration ﬁle:

cachecontrol_path="cachecontrol/CacheControl"

The default conﬁguration puts them at cachecontrol/CacheControln, where n is the
instance_id of the sched_srv hosting them. To put each in a unique for each host, add the host
name to the namespace location. For example, this deﬁnition become
cachecontrol/CacheControl-host.n, where host is the root host name and n the
instance_id of sched_srv:

cachecontrol_path = "cachecontrol/CacheControl-" + $arg(host) + "."

Coordinating operations

Ideally, sites should operate autonomously. They can perform bvconf shutdown and restart
pretty much independently of each other. However, once a site has been shut down, object
references copied to other name spaces (such as when cache ﬂushing) will become unavailable, so
for extended down time other sites should remove those objects from their name space (with
bvconf ns -U path).

Take care when using bvconf execute. If there are any conﬁguration changes that are stored in
the meta data in the database (such as when adding new service), it is best to shut down all sites,
and then execute the new conﬁguration one site at a time. If objects have been exported to remote
name spaces, they should be removed before running execute on the remote site.

Running bvconf execute reinitializes the name space, so Interaction Manager name space
objects are removed the Interaction Manager servers are restarted with imgr_conf start.

If execute is performed as an error recovery procedure (with no conﬁguration changes), other
sites do not need to shutdown if they can tolerate the down time, but they really should
execute. Regardless of which, the remote sites must still update objects. [See “Updating name
space objects across sites” on page 98.]

Avoid updating objects across sites as much as possible — within application requirements. For
example, if the multiple-site conﬁguration is a corporate top-level site pointing to sites of individual
divisions (so that each division is a “service”, with the corporate as the default), a divisional site
may ﬁnd it sufﬁcient to just periodically ﬂush the caches for other services, so avoiding having to
export its Interaction Manager objects to the other sites.

Installation and Administration Guide

BroadVision, Inc.

100

Chapter 5 Server configuration
Running a multiple-site configuration

BroadVision, Inc.

Installation and Administration Guide

6 Interaction Manager configuration

101

Conﬁguration activities are usually one-time activities that affect how the One-To-One system
operates. “HTTP servers and the Interaction Manager,” described next, provides an overview of
how the servers communicate with each other, and how to conﬁgure them for common and complex
situations. It covers these topics:

l “Directories and URLs” on page 103 details how URLs map to the document root and script

root directories for locating ﬁles.

l “Named applications” on page 104 deﬁnes named applications and describes how to have more

than one in a site.

l “Gateway applications” on page 105 explains how gateway applications route requests of the

HTTP server to the Interaction Manager servers. It also lists the gateway applications available
to One-To-One.

l “Gateways and session IDs” on page 106 describes how the HTTP servers locate the Interaction

Manager server that processes a single visitor’s requests.

l “Firewalls” on page 106 provides information about how to set up security ﬁrewalls between

the HTTP, Interaction Manager, and One-To-One server host machines.

l “Ports and IP addresses” on page 108 details how the HTTP gateways communicate with

Interaction Manager servers.

The activities in the rest of this chapter are those that you are likely to perform while conﬁguring the
system for distinctive situations, including:

l “Running multiple applications on a single CGI host,” described on page 111.

l “Conﬁguring IP masking for proxy servers” on page 111

l “Using SSL with Netscape HTTP servers” on page 112

l “Customizing the session ID format” on page 112

l “Conﬁguring the page request cache” on page 113

Some of the conﬁgurations in this section require you to edit the bv1to1.conf conﬁguration ﬁle.
For information about that ﬁle, see “Conﬁguring the One-To-One environment and services” on
page 37, and “bv1to1.conf” on page 161.

Be sure to back up bv1to1.conf before and after any configuration changes.

Anytime you change your conﬁguration, stop and then restart the Interaction Manager servers. See
“Starting the Interaction Manager” on page 42 for details.

Installation and Administration Guide

BroadVision, Inc.

102

Chapter 6 Interaction Manager configuration
HTTP servers and the Interaction Manager

HTTP servers and the Interaction Manager

Visitors make requests for information from a Web site by providing the address of the item being
requested. This is usually done with a browser by entering the universal resource location (URL)
address for the item. When the visitor enters the address, or clicks on a link that contains the
formatted address, the browser forms an HTTP request that it sends to the site’s HTTP server. For
example, a request for a speciﬁc ﬁle, might look like this:

http://bvsn.com/welcome.html

The server either gets the requested document from disk, or it executes a program which then
generates the HTML page. In this way, the server is a gateway between the requestor and the data.

Visitor

Request

HTML page

HTTP server

Request

Static HTML

Request

Dynamic HTML

Executable

In BroadVision One-To-One Enterprise, the One-To-One Interaction Manager is the executable that
manages requests for information made to the One-To-One system. When the Interaction Manager
receives a request, it determines what information has been requested, runs a script that gets the
data from the One-To-One servers, and produces the response in the form of an HTML page.

Gateway

Request

HTML page

Interaction Manager

Get data

Data

One-To-One servers

The rest of this section describes concepts that are important to understand when conﬁguring the
HTTP and Interaction Manager servers, including:

l “Directories and URLs,” described next — details how URLs map to the document root and

script root directories for locating ﬁles.

l “Named applications” on page 104 — deﬁnes named applications and describes how to have

more than one in a site.

l “Gateway applications” on page 105 explains how gateway applications route requests of the

HTTP server to the Interaction Manager servers. It also lists the gateway applications available
to One-To-One.

l “Gateways and session IDs” on page 106 describes how the HTTP servers locate the Interaction

Manager server that processes a single visitor’s requests.

l “Firewalls” on page 106 — provides information about how to set up security ﬁrewalls between

the HTTP, Interaction Manager, and One-To-One server host machines.

l “Ports and IP addresses” on page 108 — details how the HTTP gateways communicate to

Interaction Manager servers.

BroadVision, Inc.

Installation and Administration Guide

Chapter 6 Interaction Manager configuration
HTTP servers and the Interaction Manager

103

Directories and URLs

Part of the job of an HTTP server is to know how to locate the requested item. In this example,
welcome.html is probably in a subdirectory on a ﬁle server.

http://bvsn.com/welcome.html

Document root

To locate the ﬁle, the HTTP server might know that all requests to http://bvsn.com/* can be
found in the /home/WWW/http-doc directory.

Request
bvsn.com/welcome.html

Get welcome.html from
/home/WWW/http-doc/*

bvsn.com

To direct the server to the correct location, the server is conﬁgured to map all requests to the root
location to the subdirectory, similar to this CERN-style conﬁguration directive:

Pass

/*

/home/WWW/http-doc/*

The root location for the HTTP server’s HTML ﬁles is called the document root. All ﬁles that are
located in the document root hierarchy are visible and accessible to anyone who has access to the
Web server. As such, One-To-One scripts and page templates are kept in a separate location.

All static HTML and image files should be stored in or under the document root directory. This
allows the HTTP server to handle the requests instead of sending them through the Interaction
Manager server. Some sites even handle graphics through a separate HTTP server, identified by
the path to the image in the page’s HTML.

Script root

The Interaction Manager looks for scripts and page templates in a location called the script root. In a
URL to a One-To-One site, the part of the path that follows the gateway name is the path into the
script root. For example, in this URL, /broadway/scripts is a directory path in the script root
location:

http://bvsn.com/cgi-bin/inetcgi/broadway/scripts/bw_login.jsp

The script root hierarchy must be accessible to all Interaction Managers that process the same
application. Optionally, the Interaction Managers can have different script roots, but each location
must be a mirror of the other.

The script root and document root should be in different locations. In fact, for security reasons, the
script root should be in a path that is not accessible from the HTTP server. Preferably on
another system, such as behind a firewall. For information about where to locate script files for
security considerations, see “Configuring access control” on page 55.

If your site has multiple named applications, each should have its own script root.

Installation and Administration Guide

BroadVision, Inc.

104

Chapter 6 Interaction Manager configuration
HTTP servers and the Interaction Manager

Named applications

When the URL contains a request for a dynamic page, the name of the executable usually appears
after the domain name, followed by other text that qualiﬁes the information being requested. For
example, to run an executable named Financial, the URL might look like this:

http://bvsn.com/Financial...

In a One-To-One application, Financial is the name of the Interaction Manager application.

HTTP server

Financial
Interaction Manager

One-To-One servers

In addition to identifying the Interaction Manager application, assigning a name allows a site to
have multiple and different Interaction Managers that can access the same or different One-To-One
servers, depending on the site’s requirements.

HTTP server

News
Interaction Manager

One-To-One servers

Entertainment
Interaction Manager

Financial
Interaction Manager

One-To-One servers

An HTTP server that handles standard CGI processing can also route requests to multiple named
applications. However, that is not recommended in a production system. In fact, for a site with high
trafﬁc, you should use an NSAPI server instead, and an NSAPI server can support only one named
application.

Conﬁguring the
Interaction
Managers

To conﬁgure the Interaction Manager servers to recognize the name, run imgr_conf -a
configure and conﬁrm that you want to use a named application when it asks. Doing this creates
a named application conﬁguration ﬁle in the …/BVSNsmgr/ directory. For example, instead of
bvsm.cfg (the default conﬁguration name), it creates a ﬁle called appName.cfg.

Repeat this task for every machine that hosts the named application.

Conﬁguring HTTPD
installations

Each named application requires a separate HTTPD installation. See the description for your HTTP
server in “Conﬁguring the HTTP server” on page 43 for details.

Conﬁguring HTML
pages

All static HTML pages that reference your application include the path to the gateway. Edit those
ﬁles and update the links to the application to reference the gateway. For example, for a non-named
application, a typical link includes “/cgi-bin/inetcgi”. For a named application, change the
path to the gateway, such as “/cgi-bin/appName”.

BroadVision, Inc.

Installation and Administration Guide

Chapter 6 Interaction Manager configuration
HTTP servers and the Interaction Manager

105

Starting a named
application

To start an Interaction Manager server running a named application:

1. Ensure that $BV1TO1 and $BV1TO1_VAR point to the correct installation of One-To-One for this
application. This is only an issue if your site uses different One-To-One servers for different
applications.

2. Run imgr_conf and identify the installation name:

UNIX:

imgr_conf -a start -A appName

Windows NT:

imgr_conf -a start -n appName

Gateway applications

A visitor’s browser connects to an HTTP server that manages requests to the Web site. Requests to a
One-To-One application pass through a program called a gateway application. When the HTTP server
sees a request to the One-To-One application, it passes the request to the gateway, which then passes
it to the Interaction Manager servers for processing.

Request

HTTP server

Visitor’s browser

Gateway

Request

Interaction Manager

Gateway
applications

Depending on the release, One-To-One supplies gateway applications for Microsoft Internet
Information Server (IIS), Netscape Enterprise Server (NES), and standard CGI servers. Use the
gateway application software released with your copy of the One-To-One server and Interaction
Manager software because mixing versions can cause unexpected results.

HTTP Server

Microsoft Internet Information Server (can be
renamed for named applications)

HP-UX

—

Solaris

—

Windows NT

bvisapi.dll

Netscape Enterprise Server 3.0

bvensapi3.sl bvensapi3.so

bvensapi.sl

bvensapi.so

—

—

Netscape Enterprise Server other than 3.0
(such as 2.0 or 3.6)

Standard CGI, named application ﬁle (ﬁle must
be renamed)

anamecgi

anamecgi

aname.exe

Standard CGI, no application name

inetcgi

inetcgi

inetcgi.exe

If you are using a named application, the gateway application’s ﬁlename must be renamed to be the
same as the application. For example, if your application is named “news” and you are using IIS,
then you would copy and rename bvisapi.dll to news.dll.

For instructions for conﬁguring your HTTP server to use a gateway application, see

l “Conﬁguring the gateway for Netscape Enterprise Server (NES)” on page 44.

l “Conﬁguring the gateway for Microsoft Internet Information Server (IIS)” on page 46.

l “Conﬁguring the gateway for a standard CGI server” on page 48.

Installation and Administration Guide

BroadVision, Inc.

106

Chapter 6 Interaction Manager configuration
HTTP servers and the Interaction Manager

Gateways and session IDs

One-To-One Interaction Manager servers can run on different machines from those hosting the
HTTP servers. Additionally, each machine that hosts an Interaction Manager can run multiple
instances of the Interaction Manager servers, each called an engine. Engines perform the actual work
of running your One-To-One application.

A visitor’s browser connects to an engine through a program called a gateway. A gateway knows
how to connect to all the engines in an application conﬁguration. Each visitor session is managed by
the engine that created the session. As such, the gateway must return the visitor to the same engine
for all subsequent requests during the same session. This is done in part by assigning to each session
a unique session ID. Session IDs are encrypted strings that identify the visitor’s session, and encode
the unique ID of the engine that created the session.

Some sites use a DNS round robin to combine multiple machines into a single Web site, which
results in multiple IP addresses for each HTTP machine behind a common host name. This means
that a browser might get a different IP address every time it resolves the host name, which in turn
means that a different gateway must route the request to the proper engine.

Each gateway is able to locate the correct engine in the site by ﬁrst decoding the engine ID, and then
routing the request to the engine for processing. As such, it is important that every HTTP host be
able to connect to the engine hosts through a port and IP address. You can conﬁgure which ports
and addresses when you conﬁgure the Interaction Managers.

You can customize part of the session ID to include information that your application requires.
However, the first part is not customizable because it contains the locator information. [See
“Customizing the session ID format” on page 112 for details.]

Firewalls

For security, the One-To-One servers, your database, database accessing mechanism, and business
applications usually reside behind a security ﬁrewall. HTTP Web servers — because they are
network access points — usually reside outside the ﬁrewall. The Interaction Manager servers,
however, may reside on either side of the ﬁrewall. In fact, in some conﬁgurations, there are ﬁrewalls
between the HTTP, Interaction Manager, and One-To-One servers. The Interaction Manager and
One-To-One servers communicate via CORBA protocols.

HTTP server

Interaction Manager

One-To-One servers

Each HTTP host machine needs a copy of the Interaction Manager configuration files or files.
See “smgr_ip_appName” on page 109 for details. Additionally, see “Running a multiple-host
configuration” on page 93 for detail about isolating the Interaction Manager and Interaction
Manager server directories.

Each HTTP gateway is conﬁgured to know which ports the corresponding Interaction Manager is
using. You can therefore set up a ﬁrewall to only allow connection management trafﬁc on known
ports, and only between the HTTP and Interaction Manager machines. To use the port for anything

BroadVision, Inc.

Installation and Administration Guide

Chapter 6 Interaction Manager configuration
HTTP servers and the Interaction Manager

107

else, will compromise the security by allowing access to the Interaction Manager machine. You can
address this problem by putting in an intermediate machine on the internal network, where all
services are disabled, except for TCP pass-through routing.

The One-To-One Command Center hosts “bind” to the Interaction Manager host to make a
cache flush request. As such, it is necessary to open up the Orbix ports in the firewall for the
Command Center machines. See “IT_DAEMON_PORT” on page 32 for details.

Dual-homed hosts A dual-homed host is a machine that has two network connections through two different IP addresses.
When you are conﬁguring an Interaction Manager to run on a dual-homed host, use the IP address
that connects to the HTTP server as the host’s address, and use the host name that the HTTP server
would use to connect to the Interaction Manager host.

hostname: www.bvsn.com
hostname: out_http_1

126.3.2.9

0.0.0.1

hostname: out_imgr_1

hostname: in_imgr_8

0.0.0.7

1.1.1.0

hostname: in_121_8

1.1.1.4

Three hosts connected by two isolated LANs.

This Interaction Manager host configuration is:
Host name: “out_imgr_1”
IP address: “0.0.0.7”
Qualified name begins with “out_imgr_1”

On UNIX, the Interaction Manager hostname must be set to the name used by the HTTP server. For
example, in the diagram above, the host name is “out_imgr_1”. The UNIX hostname and
uname -n commands must both return that name.

% hostname
out_imgr_1
% uname -n
out_imgr_1

Remote host
conﬁguration

The Interaction Manager servers communicate with the One-To-One servers using CORBA. This
communication occurs through the port speciﬁed by the $IT_DAEMON_PORT environment variable,
which by default is 1221.

See “Running a multiple-host conﬁguration” on page 93 for details about setting up this
conﬁguration.

Installation and Administration Guide

BroadVision, Inc.

108

Chapter 6 Interaction Manager configuration
HTTP servers and the Interaction Manager

Ports and IP addresses

Page requests are routed through the HTTP server to an Interaction Manager engine. The engine
queues each request until it is handled by a worker thread. The fulﬁlled request is then routed back
through the HTTP server to the requestor.

HTTP host

Interaction
Manager
gateway

Interaction Manager host

Request queue
Request 1
Request 2
Request 3
…
Request n
New request

Worker thread

Worker thread

First engine’s
port

Second
engine’s port

To make the connection from the HTTP server to the Interaction Manager server, the One-To-One
gateway opens a TCP/IP connection to a port on the Interaction Manager host; each Interaction
Manager engine uses one port on the host. The port used by the ﬁrst engine, this is called the
preferred port. When the gateway connects to the ﬁrst engine, it uses the preferred port, and by
default, it uses the next sequentially numbered ports, one for each subsequent engine, unless you
assign other ports to the other engines.

When you have multiple HTTP hosts, each must have the same access to the ports of all
Interaction Manager hosts processing the named application. This is because different visitor
requests from the same visitor session might come from different HTTP hosts.

First HTTP host

Second HTTP host

Engine

Engine

Engine

Engine

Engine

Second Interaction Manager host

First Interaction Manager host

The conﬁguration information is speciﬁed in the bvsm.cfg ﬁle, or appropriate named application
ﬁle (such as appName.cfg), in the …/BVSNsmgr/ directory on the Interaction Manager and HTTP
hosts. To create or modify that ﬁle, you run imgr_conf -a configure and enter the
conﬁguration values at the prompts. However, the best way to identify the host machines and port
numbers within a site is with the smgr_ip_appName parameter, and then run imgr_conf -a
configure to create the conﬁguration ﬁle for the application.

BroadVision, Inc.

Installation and Administration Guide

smgr_ip_appName

Chapter 6 Interaction Manager configuration
HTTP servers and the Interaction Manager

109

The safest way to identify the Interaction Manager host machines and port numbers within a site is
with the smgr_ip_appName parameter in the bv1to1.conf conﬁguration ﬁle. This is safest
because you deﬁne the settings for the entire site in one place, making it easier to identify conﬂicts,
and to allow all Interaction Managerhosts to see the same settings. When you use this parameter, do
not change the values in the prompts when running imgr_conf -a configure.

The Interaction Manager host must be able to read the $BV1TO1_VAR/etc directory to access
the bv1to1.conf configuration file. If the host cannot see the primary $BV1TO1_VAR
directory, consider making a secondary one. [See “Running a multiple-host configuration” on
page 93.]

You need one smgr_ip_appNameparameter deﬁnition for each named application in your site. For
the default conﬁguration (no named application), the parameter is “smgr_ip_bvsm”; otherwise the
parameter is named for each named application, such as “smgr_ip_Financial” or
“smgr_ip_news”. ( Note that the name is case-sensitive and must exactly match the application
and gateway names.) For example:

smgr_ip_bvsm="255.255.255.142"
smgr_ip_Financial="255.255.255.179"
smgr_ip_news="255.255.255.69"

This parameter takes string value that is a list of the IP addresses of all the host machines for the
application. For example, to identify two machines with the default application name, include the IP
addresses separated by a semi-colon (;), like this:

smgr_ip_bvsm="255.255.255.142;255.255.255.179"

Optionally you can list the ports for the engines on each host. This example lists one port number,
which also speciﬁes that there is one engine on that host for that application.

smgr_ip_bvsm="255.255.255.142:3050

When you run imgr_conf -a configure, you will be prompted to specify the number of
engines and the starting port. If you specify them here, the values entered for the prompts will
be ignored.

Optionally, you may identify the ports — and the number of engines — to assign to by including a
range of ports. This example assigns three ports and engines to the ﬁrst host, and four to the second:

smgr_ip_bvsm="255.255.255.142:3050-3052;255.255.255.179:3000-3003"

Remember, the count of ports specifies the number of engines to use on the host for the
application. When you use this method, it take priority over the count of engines you enter in
the prompt when running imgr_conf -a configure.

You can also identify port numbers that do not fall within the same sequence, and you can mix
ranges with individual assignments.

smgr_ip_bvsm="255.255.255.142:3050,3052-3054"

CAUTION Be careful to avoid overlapping ports between applications. Each application needs its

own ports and cannot share them with other applications.

Installation and Administration Guide

BroadVision, Inc.

110

Chapter 6 Interaction Manager configuration
HTTP servers and the Interaction Manager

smgr_ﬁrst_port_minimum

When you run imgr_conf -a configure, and it cannot ﬁnd a smgr_ip_appName setting that
deﬁnes the list of ports for the current host, it scans the ports on the host and tries to determine a
range of free ports to suggest. The range will be large enough to accommodate the number of
engines deﬁned for the application. By default, imgr_conf begins scanning at port 1025. You can
set the starting port higher by including the smgr_first_port_minimum parameter in the
bv1to1.conf conﬁguration ﬁle. For example,

smgr_first_port_minimum=1080

If in the log ﬁle you see the error “Bind retry failed, errno = 125, Couldn’t initialize INETListener.”,
then you have two applications trying to access the same port. (Error 125 means “Address already in
use.”) Remember, each application needs this range of ports:

(smgr-first-port) through (smgr-first-port + count_of_engines - 1)

Conﬁguring the host machines

If your site has Interaction Manager host machines that have two network connections, such as
when using a ﬁrewall, use the IP address of the Interaction Manager host as seen from the HTTP
server. See “Dual-homed hosts” on page 107 for details.

To use the smgr_ip_appName parameter:

1. Deﬁne the parameter in the bv1to1.conf conﬁguration ﬁle, and start the One-To-One servers

with bvconf execute before you conﬁgure the Interaction Managers with imgr_conf.

2. Conﬁgure each Interaction Manager host with the same smgr_ip_appName parameter

deﬁnition in effect. When imgr_conf is running, it looks for its IP address in the
smgr_ip_appName parameter. If it ﬁnds a deﬁnition for the machine, it uses the port
assignments it ﬁnds there and determines the count of engines based on the count of ports.

Even when it finds the ports and engine count values in the smgr_ip_appNameparameter, the
imgr_conf utility still prompts you for the engines. When the Interaction Manager starts, it
takes its configuration from the smgr_ip_appName parameter, regardless of what you enter.

3. Copy the conﬁguration ﬁle from one of the Interaction Manager hosts to the HTTP host

machines. The ﬁle must be located in the …/BVSNsmgr/ directory [see “…/BVSNsmgr/” on
page 41], and have the same name as the named application. For example, if an HTTP server
supports two applications, one with the default conﬁguration and one with the name Financial,
the directory will have two ﬁles:

.../BVSNsmgr/bvsn.cfg
.../BVSNsmgr/Financial.cfg

4. If you examine these text ﬁles, you will see a line that looks similar to this:

smgr-ip-list = 255.255.255.142:3050,3055-3057,3065-3066

This setting tells the One-To-One gateway how to locate the engines that process the
application. It must be the same as the setting on the Interaction Manager host machines.

The files have other settings that are not discussed here and should not be altered manually.

Stop and then restart the HTTP server to cause it to recognize the changes.

BroadVision, Inc.

Installation and Administration Guide

Chapter 6 Interaction Manager configuration
Configuring IP masking for proxy servers

111

Configuring IP masking for proxy servers

For each page request, the Interaction Manager veriﬁes that the requestor’s IP address matches the
address that originated the session. This helps ensure that the subsequent requests are coming from
the same browser that made the initial request; it helps to ensure that a session has not been hijacked
by another system.

To accomplish this, the Interaction Manager uses a mask to compare the IP address between
subsequent requests. When doing the comparison, and bits in the mask that are set to 0 indicate the
positions that should be ignored during the comparison. For example, a mask of
255.255.255.255 means the address of the requestor must exactly match for each request, while
0.0.0.0 is means nothing in the address has to match. To permit less secure connections that allow
the client to connect through different HTTP proxies, specify a different mask. For example, a mask
of 255.255.255.0 will match all ﬁelds except the subnet address.

Running multiple applications on a single CGI host

A single CGI host can route requests for multiple named applications that each needs its own
gateway program.

An NSAPI server can support only one named application.

To conﬁgure multiple named application on a single host:

1. Run imgr_conf -a configure once for each named application, and specify the name for

each when prompted. [See “Named applications” on page 104 for details.]

2. Conﬁgure the HTTP servers and include deﬁnitions for each named application. [See

“Conﬁguring HTTPD installations” on page 104 for details.] Be sure to include gateway programs
copied from $BV1TO1/bin/anamecgi and renamed to the gateway names.

3. Copy the bvsm.cfg ﬁle, or appropriate named application ﬁle (such as appName.cfg), to the

…/BVSNsmgr/ directory on the HTTP server host.

4. Stop and restart the HTTP server to recognize the changes.

5. Start each of the named applications::

UNIX:

$BV1TO1/bin/imgr_conf -a start -A appName

Windows NT:

$BV1TO1/bin/imgr_conf -a start -n appName

The servers are now ready to accept requests.

Installation and Administration Guide

BroadVision, Inc.

112

Chapter 6 Interaction Manager configuration
Using SSL with Netscape HTTP servers

Using SSL with Netscape HTTP servers

If you plan to use a secure sockets layer (SSL) HTTP server to provide some of your page templates,
you need to be aware of the following issues.

l Requests and responses through any secure HTTP server are encrypted. As such, all content on
a secure page is encrypted, including, for example, images. Because the visitor’s browser must
decrypt the response to display it, performance will suffer unless care is taken to restrict the
usage of secure (HTTPS) requests to those cases where it is truly necessary.

Design your site with such performance goals in mind. Serve the majority of pages or templates
through ordinary HTTP, with speciﬁc links or form posts directed through HTTPS where
necessary (and the links or form posts from result pages directed back through HTTP when
appropriate). Remember, once secure mode is entered through an HTTPS request, all
subsequent templates will also use HTTPS until explicitly exited with an HTTP request.

l Sites with secure and non-secure pages often run two sets of Netscape servers, a non-SSL-

enabled set on one port for ordinary HTTP requests, and an SSL-enabled set on a different port
for HTTPS requests. Refer to the Netscape server administrative documentation for details.

l The Interaction Manager runs against SSL-enabled HTTP servers, but performance does

degrade due to the encrypting and decrypting.

Customizing the session ID format

Each visitor to a One-To-One site is assigned a unique session ID that identiﬁes the visitor to the
Interaction Manager, and thereby identiﬁes the visitor’s session. This ID appears in the URL in the
visitor’s browser, and by default looks similar to this:

www/OneToOne/SessionMgr?BV_SessionID=XA6C9JMH0218DF63&...

You may change the format of the ID to some custom-generated string. This string must contain
characters that are URL-friendly, per the CGI speciﬁcation [Universal Resource Locator, RFC 1738].
Any special characters must be URL-encoded.

To deﬁne a custom string, implement a custom session ID generator and install it in the Interaction
Manager conﬁguration:

1. Complete the implementation of the user_sid_generator.cc sample by implementing the
gen_User_SessionID() function. You can ﬁnd this ﬁle in $BV1TO1/samples/sid_gen.
The sample generates a random string:

char* User_SessionID_Generator::gen_User_SessionID() {
const char* example = "user_defined_session_id";
char randnum[16];
sprintf(randnum, "%ld", lrand48());
char* ret = new char[strlen(example) + strlen(randnum) + 1];
sprintf(ret, "%s.%s", example, randnum);
return ret;

}

2. Build your implementation by running make against the makeﬁle in the same sample directory:

% make -f Makefile.sid

BroadVision, Inc.

Installation and Administration Guide

Chapter 6 Interaction Manager configuration
Configuring the page request cache

113

3. Install your implementation with the make ﬁle. Note that this replaces a shared library in the
$BV1TO1/lib directory, and that library is owned by the root account (the one that installed
One-To-One). You have to be root user to do this step.

% make -f Makefile.sid install

4. Conﬁgure the Interaction Manager by running:

imgr_conf -a config

At the prompt that asks “Would you like to use a custom session ID generator?”, answer Y and
enter the full path to the shared library for your implementation. The library should be in one of
the directories in the $LD_LIBARY_PATH. Check the bv1to1.conf ﬁle for the deﬁnition.

5. Start the Interaction Manager (stop it ﬁrst if it is already running):

% imgr_conf -a stop
% imgr_conf -a start

Repeat the conﬁguration and restart steps for each Interaction Manager host.

Configuring the page request cache

When the Interaction Manager receives a page request, it locates and runs the appropriate script that
generates the page, and then sends the generated page to the browser to satisfy the request. Pages
on a One-To-One Web site generally contain static and dynamically-generated information. The
time that it takes to generate the page varies depending on the dynamic content that has been done.

In most One-To-One Web sites, there are pages that — while dynamically generated to match the
visitor’s proﬁle — contain the same results: multiple visitors see the same exact content. When you
can identify the conditions (the rules) where the results will be the same, you can use the Interaction
Manager request cache to satisfy the requests of multiple visitors, and thereby improve the
performance of the application.

For example, an airline Web site might offer weekly specials that are customized to different
airports. Rather than dynamically generate the page for every visitor that uses the same airport, it is
better to generate the page once for each location, cache the result, and then display the result to
every ﬂyer that uses that airport. The condition could be further reﬁned to generate different pages
for each class of frequent ﬂyer that uses the same airport: “gold” members would see one list of
specials from their airport, while, “silver” members would see a different set. However, the more
complicated the condition, the more unique pages that will have to be cached. For details about
rules, see “Cache rules” on page 117.

A page request cache contains the HTML that was generated for a page. However, the server-
side Javascript code is not cached. Any time a script must access the servers to obtain dynamic
information, such as whether or not a visitor is allowed to log in to the site, that action requires
server-side script processing, and that request cannot be cached.

Installation and Administration Guide

BroadVision, Inc.

114

Chapter 6 Interaction Manager configuration
Configuring the page request cache

Each cache has a limit to the number of generated pages that it can hold. When the limit is exceeded,
the cache removes the oldest pages and inserts the latest. You can deﬁne how many pages, and the
maximum storage size that each page may require. You can also tell the system to rebuild a page
after it has resided in the cache for a set period of time. See “Cache settings” on page 114 for details
on all these speciﬁcations.

One-To-One and Interaction Manager servers use memory caches to improve performance of
activities that access the database. For information about thos caches, see “Configuring
caching” on page 58.

The rest of this section describes these request cache topics

l “Using the cache conﬁguration ﬁle,” described next, describes how to conﬁgure the cache or

caches on your site.

l “Changing the request cache dynamically” on page 121 describes how to use the cache_utl

utility to disable or ﬂush pages from the cache.

l “Monitoring cache status” on page 122 describes how to retrieve information about the activity

of the cache while the site is live.

Using the cache conﬁguration ﬁle

The cache conﬁguration ﬁle is a text ﬁle that deﬁnes the caches, their sizes, how long generated
requests may stay in the cache, and which results to store in the cache.

The ﬁle is located in the same directory as your Interaction Manager’s conﬁguration ﬁle
(bvsm.cfg), and has the same ﬁlename, but with an .req extension instead of .cfg. The ﬁlename
varies depending on how your Interaction Manager is conﬁgured. By default, the name is
bvsm.req, but for a named application, the ﬁlename is application_name.req. See the
“Named applications” on page 104 for details about the names and locations of these two ﬁles.

If the conﬁguration ﬁle is not in the …/BVSNsmgr/ directory, no page request caching occurs for the
application.

The ﬁle is structured text that is in two sections: Cache settings deﬁne behavior and size of the caches,
and Cache list deﬁnes which requests are qualiﬁed to be put in the request cache.

Cache settings

The cache settings section contains deﬁnitions that begin with these keywords:

Timeout:size

MaxReqSize:size

MaxCacheEntry:cacheName:size

Time (in seconds) to wait to remove a item from the
cache, starting from when the item was put in the cache.

Maximum size (in kilobytes) for a cached request result.
If a generated result is larger, it will not be cached. The
minimum size is 10. This setting is limited by the amount
of memory available on the system.

Deﬁnes a request cache and sets the maximum size of
the result. This setting is limited by the amount of
memory available on the system. The minimum size is
10. See “Cache name” on page 121 for more
information. The default cache is named “DEFAULT”.

BroadVision, Inc.

Installation and Administration Guide

Cache list

Chapter 6 Interaction Manager configuration
Configuring the page request cache

115

Here are some example cache settings:

# The Interaction Manager will expire cache requests after 1,200 seconds.
Timeout:1200

# Cache generated requests that are not larger than 2048 Kilobytes.
MaxReqSize:2048

# The "default" cache will hold up to 1,000 generated requests.
MaxCacheEntry:default:1000

# Create a cache called "weeklies" that will hold up to 120 requests.
MaxCacheEntry:weeklies:120

The cache list section of the ﬁles deﬁnes which requests are qualiﬁed to be put in the cache. Each
request cache deﬁnition is a line of the following format:

type:reqPath:cacheRule:fixupPath:reqSize:timeout:cacheName

The ﬁrst two parameters are required; the rest are optional and may be omitted. All of the colons (:)
are required. The length of the line may not exceed 1,024 characters.

type

Type of item to cache: for this release, the only option is ‘J’ for Javascript.

reqPath

Path for the Javascript script, relative to the Interaction Manager script root directory.

cacheRule (optional) Rule that determines which request results to cache. See “Cache rules” on

page 117 for details. If empty, all requests meeting the typeand reqPathcriteria will
be cached.

fixupPath (optional) Path of a Javascript ﬁx up script. See “Fix up scripts,” next for details. The

path is relative to the script root. If empty, then Interaction Manager will not run the ﬁx
up script.

reqSize

timeout

(optional) A request will not be cached if the result exceeds this speciﬁed limit. If not
speciﬁed, the cache assumes the default MaxReqSize size; this value may be larger.
This setting is limited by the amount of memory available on the system.

(optional) A cached request will expire when the time it stays in the cache exceeds the
timeout limit. If not speciﬁed, the cache assumes the default Timeout value; this value
may be larger. This setting is limited by the amount of memory available on the system.

cacheName (optional) Identiﬁes which request cache will hold the result. If not speciﬁed, the request

will be put in the “default” request cache. See “Cache name” on page 121 for details.
Specifying a cache not named in the “Cache settings” creates a new cache.

Fix up scripts

The slowest part of processing a dynamic One-To-One request is retrieving information from the
One-To-One servers, especially information from the database. One of the key beneﬁts of the page
request cache is that the servers are accessed once, and the result is then stored in the generated
page in the request cache.

Installation and Administration Guide

BroadVision, Inc.

116

Chapter 6 Interaction Manager configuration
Configuring the page request cache

However, sometimes you still need additional information to be placed on the page before sending
it to the visitor’s browser. To do that, you use a “ﬁx up” script that scans the generated page in the
cache and installs any information that is personal to the visitor, such as a visitor’s name. When the
Interaction Manager receives a request for a page that is in the cache, it ﬁrst looks to see if there is a
fixupPathdeﬁnition in the speciﬁcation. If one exists, the Interaction Manager retrieves, the page,
runs the ﬁx up script on the previously generated result, and sends the modiﬁed page to the
visitor’s browser.

When you use a ﬁx up script, it should be short, and retrieve information from the Interaction
Manager memory space or from a fast system call, such as “the current time”. A ﬁx up script should
not access the One-To-One server because the slow access would defeat the purpose of the cache.

To specify a ﬁx up script, include the path to the .jsp ﬁle, relative to the Interaction Manager’s script
root. For example, this speciﬁcation — which does not use Cache rules — calls fix_weeklys.jsp:

J:/scripts/weekly_specials.jsp::/scripts/fix_weeklys.jsp:::

Here is an example of a ﬁx up script that inserts the current session ID into the links and hidden
ﬁelds on the page that include session ID information.

<%
var sl_sid = Session.Location.sessionId;
var linkMatches = _cachedBufferText.match(/BV_SessionID=@@@@[^@]+@@@@/g);
var formMatches = _cachedBufferText.match(

/hidden name="BV_SessionID" value="@@@@[^@]+@@@@"/g);

var good = true;
var numLinks = (linkMatche != null ? linkMatches.length : 0);
var numForms = (formMatches != null ? formMatches.length : 0);
var i;
var pattern = new RegExp(sl_sid, ’g’);

for (i = 0; i < numLinks; i++) {

if (linkMatches[i].search(pattern) == -1) {

good = false;
break;

}

}

if (good) {

for (i = 0; i < numForms; i++) {

if (formMatches[i].search(pattern) == -1) {

good = false;
break;

}

}

}
%>

BroadVision, Inc.

Installation and Administration Guide

Chapter 6 Interaction Manager configuration
Configuring the page request cache

117

<%= _cachedBufferText %>
<pre>
This file fixed up by fixup.jsp!!!
The new session id (from Session.Location) is <%= sl_sid %>
<%
if (good) {
%>
<font color=yellow>
All the session IDs in the buffer matched the ID from Session.Location
</font>
<%
} else {
%>
<font color=red> There were one or more mismatch errors! </font>
<%
}
%>
</pre>

<!-- Show the number of links with session ID embedded -->
<%
if (linkMatches != null) {
%>
Found these links with session ids in the buffered text:
<ol>
<%

for (var i = 0; i < numLinks; i++)

Response.write(’<li> ’ + linkMatches[i] );

Response.write(’</ol>’);

}
%>

<p>
<!-- Show the number of form hidden fields with session id embedded -->
<%
if (formMatches != null) {
%>
Found these hidden fields with session ids in the buffered text:
<ol>
<%

for (var i = 0; i < numForms; i++)

Response.write(’<li> ’ + formMatches[i] );

Response.write(’</ol>’);

}
%>

Cache rules

Cache rules deﬁne under what conditions the generated result will be cached. If you don’t deﬁne a
rule, only one result for the named reqPath will be placed in the cache. For example, an airline
Web site might offer specials that change on a weekly basis. The script for that page might be
weekly_specials.jsp. The rule for that page request might look like this which says to load the
script result into the cache:

J:/scripts/weekly_specials.jsp:::::

Installation and Administration Guide

BroadVision, Inc.

118

Chapter 6 Interaction Manager configuration
Configuring the page request cache

However, it is more likely that there would be some dynamically generated information that would
be better matched to groups of visitors. For example, the specials might be customized to different
airports. Rather than dynamically generate the page for every visitor that uses the same airport, it is
better to generate the page once for each location, cache the result, and then display the result to
every ﬂyer that uses that airport. The following example caches one page for every possible airport.
When the Interaction Manager receives a request to display the specials to the visitor, it will look
ﬁrst to see if the specials for the visitor’s favorite airport is already in the cache:

J:/scripts/weekly_specials.jsp:uprof.FAVORITE_AIRPORT::::

The problem with this example is that it gives equal weight to every airport. When there are
hundreds (or thousands) possible airports, the request cache would ﬁll up with a separate page for
each airport, and even if it could hold all of them, the cache would not be able to hold the results of
other pages.

One possible solution to this problem is to create a separate cache area just for the weekly
specials, and then let most requested airports fill up that cache, and leave the default cache to
handle all other page requests. See “Cache name” on page 121 for details.

A better implementation might be to cache only the results for the most popular airports. This
would cause the weekly special pages for lesser airports to be generated for each request instead of
retrieving them from the cache. The response for those would be slower, but by deﬁnition, they
shouldn’t be requested as often, and would likely get pushed out of the cache as newer requests
were made. This example caches the specials for three airport only, the specials for the other get
regenerated for each request.

J:/scripts/weekly_specials.jsp:uprof.FAVORITE_AIRPORT=SFO#DFX#BOS::::

The rule could be further reﬁned to generate different pages for each class of frequent ﬂyer that uses
the same airport: “Gold” members would see one list of specials for their airport, while, “Silver”
members would see a different set. However, the more complicated the condition, the more unique
pages that will have to be cached. So, after determining that the “Gold” members visit the site in a
higher percentage than the others, you might decide to only cache the pages for those Gold
members who use the three most common airports:

...:uprof.FAVORITE_AIRPORT=SFO#DFX#BOS & user.COMMUNITY=Gold::::

Remember, the length of the line may not exceed 1,024 characters.

Cache rule syntax

Each rule is a list of request predicates separated by ampersands (&) in this format:

ReqPred_1 & ReqPred_2 & ... & ReqPred_n

Each request predicate can be:

l Request variables passed in with the HTTP request, typically a variable set and passed from the

page that generated the link that the visitor chose.

l Proﬁle attributes retrieved from the visitor’s proﬁle.

l Session proﬁle variable that identiﬁes session proﬁle information.

l Account information identifying visitor information that is not speciﬁc the proﬁle attributes.

l System information retrieved from the Interaction Manager.

BroadVision, Inc.

Installation and Administration Guide

Chapter 6 Interaction Manager configuration
Configuring the page request cache

119

The rest of this section describes the predicates.

Request variables A predicate based on a request variable looks for the variable in the information passed to the

Interaction Manager in the HTTP request. It is typically a variable set and passed from the page that
generated the link that the visitor chose to make the request. Each request variable predicate can
have one of the following forms:

req.requestName
req.requestName = value
req.requestName = value1 # value2 # ... # value_n

The ﬁrst form indicates to cache all values for the speciﬁed request variable, including when the
variable is undeﬁned or is null. For example, a Javascript page might deﬁne

var mode = Request.value("mode");
mode = "Register";

To load all the results into the cache:

J: ... :req.mode: ...

The other forms of the predicate specify cases to cache: when the value meets a speciﬁc criteria. For
example, this request is only cached when the value of mode is “FirstLook”:

J: ... :req.mode=FirstLook: ...

There are two special case “values”:

l <undef> identiﬁes when the variable is undeﬁned.

l <null> identiﬁes when the request is deﬁned but is an empty string.

For example, when the action variable in the BroadWay login script is undeﬁned this rule caches
all of the possible mode results (which for that particular script is either “Register”):

J:.../bw_login.jsp:req.action=<undef> & req.mode: ...

The reason you want to cache the BroadWay login script when the action is undeﬁned is because
every visitor sees the same results in that condition: the same HTML result. But, once action is
deﬁned, the bw_login.jsp script requires server-side Javascript processing to determine if the
visitor may log in. When ever a result requires server-side processing, the result cannot be cached.

Proﬁle attributes A predicate based on a visitor proﬁle attribute caches each variation of the attribute’s value,

depending on which of the following forms you use:

uprof.userProfileName
uprof.userProfileName = value
uprof.userProfileName = value1 # value2 # ... # value_n

The ﬁrst form indicates to cache all values for the speciﬁed attribute, including when the attribute is
null (userProfileName=<null>).

For example, to load proﬁles from California, Nevada, and Oregon into the cache:

J: ...:uprof.STATE=CA#NV#OR: ...

Installation and Administration Guide

BroadVision, Inc.

120

Chapter 6 Interaction Manager configuration
Configuring the page request cache

When the attribute value is based on an ENUM, you must specify the index to the item (zero based)
in the ENUM deﬁnition, instead of the attribute value. For example, the AGE_RANGE data type
deﬁnes these values:

"Under 15"
"15-17"
"18-24"
"25-34"
"35-44"
"45-54"
"55-64"
"Over 65"

To ﬁll the cache with results from the “35-44,” “45-54,” and “Over 60” ranges, specify 4, 5, and 7
indices:

J: ... :uprof.AGE_RANGE=4#5#7: ...

Session proﬁle
variable

The sprof predicate identiﬁes session proﬁle information.

sprof.sessionProfileName
sprof.sessionProfileName = value
sprof.sessionProfileName = value1 # value2 # ... # value_n

Account
information

The user predicate identiﬁes visitor information that is not speciﬁc the proﬁle attributes.

user.COMMUNITY

Identiﬁes One-To-One Command Center communities to cache. Requires
at least one communityName value.

user.ID

The visitor’s ID value. Avoid using this option, it will quickly ﬁll a cache.

user.IS_ACTIVE

Indicates if the visitor’s account is active or not.

user.IS_REGISTERED

Indicated whether or not the visitor is registered.

user.USERNAME

The visitor’s login name. Avoid using this option, it will quickly ﬁll a cache.

All of these predicates accept values conditions, though user.COMMUNITY requires at least one,
speciﬁc community to cache.

user.COMMUNITY = communityName
user.COMMUNITY = community1 # ... # community_n

A site might have communities that indicate the caliber of the visitor, such as Platinum, Gold, and
Bronze. This example caches results for each of the three communities:

J:...:user.COMMUNITY=Platinum#Gold#Bronze:...

System
information

The sys predicate identiﬁes system information. Currently, only the service name is available.

sys.SERVICE
sys.SERVICE = serviceName

BroadVision, Inc.

Installation and Administration Guide

Cache name

Chapter 6 Interaction Manager configuration
Configuring the page request cache

121

By default, the system has one page request cache named “default”. Internally and for reporting
purposes, the actual name of the cache is “REQ-cacheName”, such as “REQ-DEFAULT”. The
default cache is the one accessed with BV_GenericCacheMgr::set_default_cache_size().

You can deﬁne additional caches with the MaxCacheEntry deﬁnition. Deﬁne new caches when you
want the contents of the cache to be speciﬁc to a category of results. Keep in mind that generated
pages are removed from a cache when their Timeout has expired, or when newer pages push the
oldest page out of the cache. If you have pages that don’t change as often as others, but still are
accessed by many visitors, consider putting those results in a slower cycling cache so that the faster
cycling pages don’t push them out.

For example, if an airline site has weekly specials, the generated pages are not going to change or
timeout as quickly as other pages. To keep them in the cache longer, create a separate cache area just
for the weekly specials, and leave the default cache to handle all other page requests. This example
creates a cache named “WEEKLY_SPECIALS” and demonstrates a cache rule that uses it.

MaxCacheEntry:WEEKLY_SPECIALS:100

J:/scripts/weekly_specials.jsp:uprof.FAVORITE_AIRPORT::::WEEKLY_SPECIALS

Changing the request cache dynamically

To ﬂush a request cache, use the cache_utl utility, and specify “request_cache” as the
-e cacheName option. For example, this reloads all caches and re-reads the bvsm.req
conﬁguration ﬁle:

% cache_utl -e request_cache

Optionally you can identify the request cache you want to ﬂush with the -d option. For example, to
only reload the default cache:

% cache_utl -e request_cache -d REQ-DEFAULT

You can also use the -a applicationName option to identify an application’s cache. In this case,
the name should match the name assigned to the .req ﬁle. For example, if the application name is
“news”, the conﬁguration ﬁle is “news.req”, and the cache_utl command is:

% cache_utl -a news -e request_cache -d REQ-DEFAULT

The -d option also takes “dump” as a command to write the rules currently in the cache to the log
ﬁle. When logging is on, you can log the rules with the dump argument:

% cache_utl -e request_cache -d dump

To do this, Interaction Manager logging must be set to at least level 3 (information) in the
.bvlog.conf ﬁle.

18

0:3

DEFAULT

// Info for Interaction Manager

To reconfigure the logging level at runtime without restarting the servers, send the appropriate
signal to the bvsmgr server. See “Log signal” on page 168 for details.

Installation and Administration Guide

BroadVision, Inc.

122

Chapter 6 Interaction Manager configuration
Configuring the page request cache

Monitoring cache status

You can monitor the request cache status with the bvconf utility’s monitor command. Specify the
name of the cache that you want to monitor in the -L option; for the default cache, use
“REQ-DEFAULT.*”.

% bvconf monitor -p bvsmgr -m BV_CACHE_STAT [ -A appName ] \

-L "REQ-DEFAULT.*"

See “Report options” on page 148 for details about the options.

You can reﬁne the monitor information by specifying any of these -L parameters:

REQ-DEFAULT-SIZE

Count of items currently in the cache.

REQ-DEFAULT-HIT

Count of requests found in the cache.

REQ-DEFAULT-MISS

Count of requests that were not in the cache.

REQ-DEFAULT-SWAP

Count of items that got swapped out of the cache. Useful for
identifying a cache that is too small.

REQ-DEFAULT-MAX

Maximum size of the cache in bytes.

For example, to only monitor the cache hits, include REQ-DEFAULT-HIT:

% bvconf monitor ... -L "REQ-DEFAULT.REQ-DEFAULT-HIT"

Alternately, this version shows the speciﬁed labels from both BV_CACHE_STAT and BV_SRV_STAT,
once every two seconds:

% bvconf monitor -p bvsmgr -M -L CONN,SESS,CGI,REQ-DEFAULT-HIT -s 2

In the above example,

l CGI tells you the total number of requests an Interaction Manager has served.

l REQ-DEFAULT-HIT tells you the total number of requests that hit the cache.

l The delta between the above two is the number of missed requests, plus the number of

uncachable requests.

BroadVision, Inc.

Installation and Administration Guide

7 Commerce-specific configuration

123

The conﬁguration activities described in this chapter are speciﬁc to the One-To-One commerce
features. These conﬁgurations are not essential for starting and running the BroadVision
One-To-One Enterprise, but are required for some commerce-speciﬁc tasks.

One-To-One Commerce™ is a separate product that incorporates some of these configurations.
See the documentation for that product for information about its specific configuration
activities.

Commerce conﬁguration activities are usually one-time activities that affect how the One-To-One
system operates. The activities in this chapter reﬂect those that you are likely to perform while
conﬁguring One-To-One to use the commerce features, including:

l “Installing AVP Taxware” on page 124, described next.

l “Conﬁguring the Taxing system” on page 126.

l “Computing Shipping Costs” on page 127.

l “Conﬁguring order numbers” on page 128.

l “Conﬁguring microtransaction logging” on page 129.

l “Conﬁguring payment handling” on page 130.

For One-To-One server-speciﬁc conﬁguration settings, see Chapter 5, “Server conﬁguration.” For
Interaction Manager conﬁgurations, see Chapter 6, “Interaction Manager conﬁguration.”

Most of the conﬁgurations in this section require you to edit the bv1to1.conf conﬁguration ﬁle.
For information about that ﬁle, see “Conﬁguring the One-To-One environment and services” on
page 37, and “bv1to1.conf” on page 161. Before you can conﬁgure the One-To-One services, you
must install the software. See Chapter 2, “Installation.” Anytime you change your conﬁguration, be
sure to restart One-To-One. See “Restarting your site” on page 139 for details.

Be sure to back up bv1to1.conf after any configuration changes.

Installation and Administration Guide

BroadVision, Inc.

124

Chapter 7 Commerce-specific configuration
Installing AVP Taxware

Installing AVP Taxware

For instructions on installing the AVP Taxware package, see the manuals that come with the
Taxware package. For Windows NT, especially review, “Setting Up the System”, “Operating Under
Windows”, and “Operating Under Windows NT”. However, in summary, you need to perform
these steps:

On UNIX, if you retrieve any of the Taxware files with ftp, use ASCII mode, so that there are no
control-M characters in the files. Also, after using ftp, all Taxware ﬁlenames are in upper case,
convert all ﬁlenames to lower case, for example, TAX010.C should be tax010.c.

1. Copy the Softfocus Btree/Isam software (comes from Taxware) to your system. Compile the

source to create a libbtv3.a.

2. Copy the Taxware source and data ﬁles from the AVP diskettes to your system.

3. Deﬁne the environment settings to point to the AVP directories and ﬁles:

On UNIX, set the $AVPIN, and $AVPOUT environment variables to point to the correct AVP
directories.

setenv AVPIN /import/avp3.0/indata
setenv AVPOUT /import/avp3.0/outdata

On Windows NT, in the AVP documentation you will ﬁnd instructions for creating AVPTAX.INI,
a conﬁguration ﬁle to be placed in your Windows NT system directory (with the other
application .INI ﬁles). Here is an example of AVPTAX.INI:

[AVPTAX]
AVPOUT=f:\avptax\outdata
AVPIN=f:\avptax\indata
AVPTEMP=f:\avptax\temp
AVPAUDIT=f:\avptax\audit

After creating the ﬁle, create the data for the indata and outdata directories. Do this by
unzipping and copying the data ﬁles from the DATA FILES and NEWMAST diskettes
respectively, and by running TAXWIN, which is supplied by AVP, and selecting
Load->Product Files and then Load->Tax Files.

BroadVision, Inc.

Installation and Administration Guide

Chapter 7 Commerce-specific configuration
Installing AVP Taxware

125

4. Move all Taxware *.h and *.c ﬁles into a directory where you can build the Taxware

executables. Build all the executables as listed in the makeﬁle that comes with Taxware. To be
compatible with One-To-One, comment out these #defines in taxset.h:

/*
#define SYSCTRL_MSDOS
#define SYSCTRL_USE_STEP
#define SYSCTRL_MULTI_USER
#define SYSCTRL_ORACLE
#define NO_NEGATIVE_RATES
#define SYSCTRL_SINGLE_OPEN
#define TAX_API_UPGRADE
*/

Uncomment these #defines:

#define SYSCTRL_UNIX    /* also use for OPEN VMS */
#define SYSCTRL_USE_JURIS
#define SYSCTRL_USE_PRODUCT
#define SYSCTRL_USE_ERRFILE
#define SYSCTRL_AUDFTYP LONGAUD

Your build should create such executables as tax006, tax020, tax021, tax911, and so on.

5. Move all non-source ﬁles (data ﬁles) to the $AVPIN directory. Make sure the environments
mentioned in Step 3 are set. The $AVPOUT directory should initially be empty. The $AVPIN
directory should have a list of ﬁles similar to these:

% ls $AVPIN
newmast
parm006
parm007
parm008

parm021
parm022
parm025
parm030

parm999
prodseq
taxbyitm
taxcuspd

taxexczp
taxfrcpd
taxfrtpd
taxjurcd

taxjurpd
taxprizp
taxrntpd
taxsrcpd

taxstapd
taxtest
taxupdt
taxvalzp

6. At a minimum, perform these steps:

a. Run tax006 to load in the product code ﬁle, this requires the prodseq ﬁle in your $AVPIN

directory.

b. If there is a totally new tax master ﬁle (named newmast), run tax021. The newmast ﬁle

must be in the $AVPIN directory.

c.

If there are updates for the Tax Master ﬁle, copy that ﬁle to $AVPIN and rename it as
taxupdt, then run tax020.

After Step c, your $AVPOUT directory should contain a list of ﬁles, like the list below:

%ls $AVPOUT
prdcnpf.dt
prdcnpf.nx

prdlopf.dt
prdlopf.nx

prdstpf.dt
prdstpf.nx

taxcnpf.dt
taxcnpf.nx

taxlopf.dt
taxlopf.nx

taxstpf.dt
taxstpf.nx

You might also want to run other executables, such as tax911 which lists the Jurisdiction code ﬁle.
Consult the Taxware manuals for information about the executables.

Installation and Administration Guide

BroadVision, Inc.

126

Chapter 7 Commerce-specific configuration
Configuring the Taxing system

Configuring the Taxing system

One-To-One computes taxes for purchases with its Taxing system. The Taxing system is able to
determine taxes for a purchase by applying local taxes, as well as any other taxes determined by the
destination of the product shipment. The system does this by using an external tax computation
utility, such as the AVP tax program. The system is also capable of computing a simple, ﬂat tax for
all items in an invoice. You can specify how One-To-One computes taxes by changing the taxing
settings in the bv1to1.conf conﬁguration ﬁle.

For information about installing AVP Taxware and configuring it for use with One-To-One, see
“Installing AVP Taxware” on page 124.

AVP tax program If you are using the AVP tax program, it must be installed before you start One-To-One with AVP

taxing enabled. After AVP is installed, edit the bv1to1.conf conﬁguration ﬁle and edit the AVP
variables to point to the location where you installed the AVP software. If you are not using AVP, the
variables must be undeﬁned.

#AVPIN="/import/avp3.0/indata"
#AVPOUT="/import/avp3.0/outdata"
#AVPAUDIT="/import/avp3.0/audit"
#AVPTEMP="/import/avp3.0/tmp"

The AVP tax program generates a log ﬁle, taxaulpf, that can grow quite large over time.
One-To-One does not use this ﬁle; periodically, you should truncate this ﬁle to free up disk space.
This ﬁle is located in the $AVPAUDIT directory. To truncate the ﬁle:

UNIX:

cat /dev/null > $AVPAUDIT/taxaulpf

Windows NT:

cat NUL: > $AVPAUDIT/taxaulpf

Line-item taxing

Traditionally, One-To-One computed taxes for purchases for the entire invoice, and then stored the
tax amount with the invoice. In the bv1to1.conf conﬁguration ﬁle, setting the tax_calc_mode
parameter to true (1) causes the SalesRep and Order Fulﬁllment systems to compute and store the
taxes on a per-line-item basis. When the setting is false (0), taxes are computed on a destination
level, and are then stored with the invoice total information. This setting globally affects all services
within the site. To turn it on:

tax_calc_mode="1"

Flat tax rate

Instead of using a complex tax calculating system which calculates taxes based on destination and
other criteria, you can specify a simple ﬂat tax by specifying the amount with the
simple_tax_rate parameter in the bv1to1.conf conﬁguration ﬁle. To specify a ﬂat tax, specify
a value with at least two decimal places. For example, to specify a rate of 8.75%:

simple_tax_rate="0.0875"

If you omit this setting from bv1to1.conf, or comment it out, One-To-One uses the Taxing system
to compute complex taxes for an order.

When using the AVP tax program and a flat tax rate, you must undefine $AVPIN.

BroadVision, Inc.

Installation and Administration Guide

Chapter 7 Commerce-specific configuration
Computing Shipping Costs

127

To turn taxing off, set simple_tax_rate to 0.00:

simple_tax_rate="0.00"

This setting globally affects all services within the site.

Computing Shipping Costs

The One-To-One Order Management system computes shipping costs based on the criteria you
specify in the bv1to1.conf conﬁguration ﬁle. These settings affect the shipping computation for
the entire site; all services must use the same method for computation. If you migrated your
conﬁguration ﬁle from an earlier version One-To-One, you might have to add these settings.

Flat shipping rate By default, One-To-One computes shipping based on a simple ﬂat rate of 7.50%. To change this ﬂat

rate to another value, declare the new rate and specify a value with at least two decimal places.

simple_ship_rate="7.50"

If you want to provide your own shipping implementation, omit this setting from bv1to1.conf, or
comment it out. Then One-To-One will use the Shipping system to compute complex rates for an
order.

Line-item or
invoice
destinations

One-To-One can compute the shipping costs of an invoice on a per destination or a per line-item
basis. By default, the computation is on a per-destination basis. To conﬁgure One-To-One to use this
feature, edit bv1to1.conf and locate the new ship_calc_mode parameter to the Site
Conﬁguration section. To compute the charge on a line-item basis:

ship_calc_mode="1"

To turn this feature off (invoice level computation), set the value to zero (0).

The SalesRep computes shipping costs on an invoice-level or line-item level as determined by the
ship_calc_mode setting as follows:

l For invoice-level destinations (ship_calc_mode="0" or not speciﬁed), the SalesRep calls

BV_Shipping::calculate() to compute the cost for each destination.

l For line-item destinations (ship_calc_mode="1"), the SalesRep calls

BV_Shipping::calculate_per_item() to compute the cost for each line-item. It then stores the cost
for each item in the SHIP_COST column of the BV_PRICED_ITEMS_TABLE table.

Default shipping
destination

The SalesRep determines a visitor’s default destination (shipping address) from the visitor’s
registered proﬁle. However, if the visitor has not registered that information, the system uses
default values (which different for each localized version of One-To-One):

default_country="US"
default_city="Los Altos"
default_locality="CA"
default_postal_code="94022" # Zip code for U.S.A.

# May be empty ("")
# State abbreviation for U.S.A.

Installation and Administration Guide

BroadVision, Inc.

128

Chapter 7 Commerce-specific configuration
Configuring order numbers

If the default_country value is “US”, the destination is ﬁlled with values appropriate for the
U.S.A. (a US_Location data type). Otherwise, the destination is ﬁlled with an appropriate
international location speciﬁed by the value (an Intl_Location data type). If the
default_country setting is not present, the other settings are ignored. In this situation if the
visitor has not registered a destination, the system defaults to a U.S.A. location.

Configuring order numbers

An order number begins with a preﬁx, has a number that increments to distinguish the order other
similar orders, and ends with a sufﬁx. By default, the initial order number for the system is
“abc-000000000-xyz”. You can change the format of the number by changing the values in the
BV_INVOICE_CONFIRMATION_TABLE table. This table stores the information about order
numbers, including the format, the range of numbers to cache, and the next number to generate.

At least one row with the service name “_reserved_” must exist and applies to all services. When
the order management system starts up, it generates a set of order numbers and caches them, and
updates BV_INVOICE_CONFIRMATION_TABLE to contain the information about how to generate
the next set of numbers. Here are the attributes in that table:

Attribute

Column

Semantics

SERVICE

varchar(25) Name of service. At least one records contains “_reserved_” which

contains the information for the site.

PREFIX

varchar(5) Preﬁx, up to ﬁve characters, prepended to the order number. May be

empty. The default is “abc-”.

SUFFIX

varchar(5) Sufﬁx, up to ﬁve characters, appended to the order number. May be

empty. The default is “-xyz”.

INCREMENTOR varchar(15) Next incremental value to use when creating order numbers. The default
is “000000000”. When this number overﬂows, such as after “999999999”,
it returns to zeros.

RANGE

integer

Count of new order numbers that the order management system creates
and caches. The default is 250.

The SERVICE attribute is reserved for possible future support of service-specific IDs. For now,
all services must use the same order numbers.

The PREFIX and SUFFIX values are optional. If you leave the strings empty, no values will be
assigned. The INCREMENTOR maximum value is determined by the count of digits you assign to
the string in the column. For example, if you assign “000” the largest number is “999”. When the
INCREMENTOR overﬂows, it rolls back to zeros.

For returned items the Order Fulfillment system assigns “ret-” as the prefix to identify returned
orders. Programmers can override this string. See the description of the BV_OrderReturn data
type in the API Reference.

BroadVision, Inc.

Installation and Administration Guide

Chapter 7 Commerce-specific configuration
Configuring microtransaction logging

129

The table is deﬁned in the $BV1TO1/bin/scripts/fulfil_db.sql SQL ﬁle, similar to this:

create table BV_INVOICE_CONFIRMATION_TABLE(

SERVICE varchar(25) primary key,
PREFIX varchar(5),
SUFFIX varchar(5),
INCREMENTOR varchar(15),
RANGE integer);

insert into BV_INVOICE_CONFIRMATION_TABLE

values(’_reserved_’, ’abc-’, ’-xyz’, ’000000000’, 250);

To change the format of the order numbers, change the values in the insert statement and apply the
changes to the database. See the Database Administrator’s Guide for information about applying SQL
changes to the database.

Configuring microtransaction logging

Microtransactions provide a way to record low cost online transactions of digital goods when
payment authorization can be postponed, and when visitor conﬁrmation, invoicing, and receipt
generation is not justiﬁed — such operations require many steps to ensure the transaction quality
and authenticity. Editorial content is an example of content typically sold as a microtransaction.

Applications are responsible for enforcing a visitor’s ability to use microtransactions. This
especially applies to “anonymous” guest visitors who are unable to establish payment methods.

Turning on
microtransaction
logging

Microtransaction logging is off by default. You can turn it on by modifying the
$BV1TO1_VAR/etc/.bvlog.conf conﬁguration ﬁle. [For details about this ﬁle, see “.bvlog.conf” on
page 184.] To turn microtransaction logging on, add the following line to the conﬁguration ﬁle:

19

0:5

mtlog%

The line tells One-To-One to log microtransactions to
$BV1TO1_VAR/logs/hostname/mtlog.YYYYMMDD; where hostname is the name of the host
machine, and YYYYMMDD is the date of the log ﬁle.

The microtransaction log ﬁle is a text ﬁle that contains the records of the microtransactions. To use
this data, see the Database Administrator’s Guide.

See “Conﬁguring payment logging” on page 135 for information about payment transactions.

Installation and Administration Guide

BroadVision, Inc.

130

Chapter 7 Commerce-specific configuration
Configuring payment handling

Configuring payment handling

Payment handling is the technique for doing payment authorization and settlement for invoices.
Payment authorization is the permission to charge an amount to a consumer’s credit card, and
settlement is a post-authorization action that settles a previously authorized transaction.

Payment handlers Payment handling usually involves communication with external systems that perform the actual

credit card authorization or settlement, such as with a ﬁnancial establishment or credit card
processing service through a payment handler. One-To-One payment handlers are daemon processes
that asynchronously poll the database looking for payments to authorize or settle. The One-To-One
pmthdlr_d process handles authorization, while the pmtsettle_d process performs settlement.

You can have multiple authorization daemons to speed up the throughput and latency times for
doing authorizations.

The payment daemons use payment handler objects to interact with the system through public
One-To-One server APIs. You can create new payment handler objects by writing classes that
implement the payment authorization and settlement methods required by the payment daemons.
See the API Reference for details about creating a custom payment handler.

Payment
processing
methods

To communicate with the external ﬁnancial system, each handler uses a speciﬁc payment processing
method. Sites can have up to 20 payment processing methods, and each service can use a different or
multiple methods. One-To-One comes with these three methods:

l omni uses Verifone’s Omnihost service. When you use Omnihost, you also need to conﬁgure

omnihost.cfg to reﬂect the conﬁguration for communicating with the bank when authorizing
credit card purchases. For information about changing the ﬁle, see “Conﬁguring Omnihost
(Solaris only)” on page 135. (Omnihost is not available on the HP-UX and Windows NT
platforms.)

l test doesn’t perform an ﬁnancial transaction. Instead, it authorizes a request as if permission
had been granted. Use this method during application development, or if you intend to pull the
invoices and perform the real payment transaction later.

Payment types

Each visitor that makes a payment transaction speciﬁes a payment type for the transaction: the mode
of payment, such as Visa, MasterCard, or Discover credit card. Within a One-To-One site, payment
types are mapped to integers that are consistent throughout the site. All payment types are available
to the entire site, and all services in the site follow the same mapping, even if they don’t use the
same payment types.

The rest of this section describes how to conﬁgure the payment handling system, including:

l “Conﬁguring payment types” on page 131

l “Conﬁguring payment handlers” on page 131

l “Conﬁguring payment logging” on page 135

l “Conﬁguring Omnihost (Solaris only)” on page 135

BroadVision, Inc.

Installation and Administration Guide

Conﬁguring payment types

Chapter 7 Commerce-specific configuration
Configuring payment handling

131

Each payment type available within the site has an integer that identiﬁes it. All services in the site
follow the same type-to-integer mapping, even if they don’t use the same payment types. To
establish the payment types for your site, you need to either:

l modify the meta_data.sql SQL script that maps the integers to the types, and then reinstall
the One-To-One database, or, if you have data in your database and do not want to lose it:

l modify “meta” data stored in the BV_PMT_TYPES table.

CAUTION Once you have real orders in your site, you cannot change the mappings. For example,
if at a later time, no site supports the type that maps to type number 0, do not change the
mappings to remove that type. To add new types, modify the file and append a new insert
statement for the new type.

Whichever method you choose, use the $BV1TO1/bin/scripts/meta_data.sql script as your
guide. In that ﬁle you will ﬁnd statements for inserting the payment types data into the
BV_PMT_TYPES table, similar to this:

insert into BV_PMT_TYPES VALUES(0, 'Visa')
insert into BV_PMT_TYPES VALUES(1, 'MasterCard')
insert into BV_PMT_TYPES VALUES(2, 'Discover')

The ﬁrst payment type ID must be 0, and each subsequent type must be numbered sequentially
after that.

If you are going to modify the script directly, do so and then run
bvconf execute -a install_all to read the changes and replace all One-To-One meta data.
However, if you have data in your database, create a separate SQL ﬁle that inserts the data directly
into the table.

Once that is done, you can modify the bv1to1.conf conﬁguration ﬁle and identify which services
use which payment types.

Conﬁguring payment handlers

To conﬁgure the payment handlers, you need to identify the payment processing methods, and
conﬁgure the payment handling daemons. Do that by modifying the bv1to1.conf conﬁguration
ﬁle to specify the payment handler conﬁguration. [See “bv1to1.conf” on page 161 for detailed
information about the conﬁguration ﬁle.]

Obtaining billing addresses

One-To-One does not automatically store a visitor’s billing address with the payment information in
the BV_PAYMENT table.

pmt_addr_from_profile="0"

# Do not store address automatically

Installation and Administration Guide

BroadVision, Inc.

132

Chapter 7 Commerce-specific configuration
Configuring payment handling

To store the information automatically, change this setting to “1”. When this setting is on, retrieves
the visitor’s registered address in the BV_USER_PROFILE table and stores it with the payment
information in the BV_PAYMENT table.

BV_USER_PROFILE

BV_PAYMENT

ADDRESS

CITY

STATE

ZIP

CARD_ADDR

CARD_CITY

CARD_STATE

CARD_ZIP

Description

Address

City

State or province

Zip or postal code

COUNTRY

CARD_COUNTRY

Country

Conﬁguring payment methods

To specify which payment methods process which payment types, assign the methods with the
default_pmt_methods and pmt_methods directives. The default_pmt_methods directive
assigns default handlers available throughout the site. For example, the following makes payment
types 0 and 1 use the Omnihost method, while type 2 uses the CyberCash method.

default_pmt_methods="0=omni, 1=omni, 2=cyber"

Each service can use the default handlers speciﬁed by the default_pmt_methods directive, or
specify their own handlers with the pmt_methods directive. For example, the BestBuyClothing
service in the following example uses the same payment types that the site in the previous example
uses, but uses a different method — CyberCash — for payment type 1:

service BestBuyClothing {

parameter
email_address = "mgr@bestbuyclothing.com"
...

pmttype_id = "0, 1, 2"
# specify non default payment processing methods here if needed
pmt_methods = "0=omni, 1=cyber, 2=cyber"

}

Conﬁguring payment daemons

The Payment system has three daemons that perform tasks associated with payment handling:

l pmtassign_d — the payment archive daemon routes invoice and payment records to the

archives.

l pmtsettle_d — the payment settlement daemon settles authorized transactions

l pmthdlr_d — the payment authorization daemon acquires authorization for a payment

To conﬁgure these daemons for your site, modify your bv1to1.conf conﬁguration ﬁle.

BroadVision, Inc.

Installation and Administration Guide

Chapter 7 Commerce-specific configuration
Configuring payment handling

133

Payment archive
daemon

Every site needs one payment archive daemon to route payment records to the archives. Do that
with the payment archive (pmtassign_d) daemon. The payment assignment daemon periodically
checks the invoices table looking for records with completed payment transactions, and then moves
those records into an archive table. It only moves records whose InvoiceState matches one of the
values in the archive_states string, and must have passed its fulﬁlled date for the count of days
speciﬁed by archive_period.

daemon pmtassign_d {

parameter
archive_period="1"
archive_states="_OrderComplete, _OrderPartiallyComplete,

# Archive period (days since fulfill date)

sleep="3600"
host="mars”

}

_OrderCancelled, _OrderReturnComplete"

# Seconds to wait between checks.
# Run on the mars host machine

Do not break the archive_stateswith a newline; it must be on one line. The line was broken in
this documentation to fit on the page.

The archive_states parameter only recognizes the four states shown in the example. If you do
not want to archive invoices in one of these states, remove the state from the string.

Payment
settlement
daemon

Every payment process method in use in your site needs one, and only one, payment settlement
daemon (pmtsettle_d) per payment method to settle authorized transactions. The payment
settlement daemon periodically checks the database for orders of the associated payment processing
method that need to be settled.

daemon pmtsettle_d {

parameter
pmt_method="omni"
sleep="180"
host="mars”

}

# The associated payment processing method.
# Seconds to wait between checks.
# Run on the mars host machine

Payment
authorization
daemon

For each payment processing method, you need one or more authorization daemon (pmthdlr_d) to
periodically acquire the authorization when a request is made. Each authorization daemon within a
site must have a site-unique proc_num that identiﬁes that daemon. The identiﬁcation numbers are
sequential integers starting with "1" for the ﬁrst one.

daemon pmthdlr_d {
parameter
proc_num="1"
pmt_method="test"
sleep="60"
host="jupiter”

}

# Set to 2,3, etc. for additional handlers.
# The associated payment processing method.
# Seconds to wait between checks.
# Run on the jupiter host machine

Earlier version of One-To-One used pmt_type instead of pmt_method. This version accepts
pmt_type to allow you to use your old conﬁguration ﬁle. Similarly, other parameters from earlier
versions that aren’t listed are also accepted, but they are no longer used and are ignored.

If you write your own payment handler, the pmt_method name should be the same as the one
returned by the method_name() member of your external handler class.

Installation and Administration Guide

BroadVision, Inc.

134

Chapter 7 Commerce-specific configuration
Configuring payment handling

You can improve performance by speeding up throughput and reducing latency times of
authorization requests by deﬁning multiple payment authorization daemons. The following
example demonstrates three different payment authorization daemons and two settlement daemons
supporting two different processing methods. Note that each payment authorization handler has its
own, unique, sequential ID.

# Multiple authorization processes allowed per processing method.
daemon pmthdlr_d {
parameter
proc_num="1"
pmt_method="omni"
sleep="20"

# Set to 2,3, etc for additional handlers
# Support Omnihost processing method

}
daemon pmthdlr_d {
parameter
proc_num="2"
pmt_method="cyber"
sleep="20"

}
daemon pmthdlr_d {
parameter
proc_num="3"
pmt_method="cyber"
sleep="20"

}

# Support CyberCash processing method

# Support CyberCash processing method

# Only one payment settlement process supported per processing method.
daemon pmtsettle_d {

# Payment settlement process

parameter
pmt_method="omni"
sleep="20"

}
daemon pmtsettle_d {

parameter
pmt_method="cyber"
sleep="20"

}

# Payment settlement process

BroadVision, Inc.

Installation and Administration Guide

Chapter 7 Commerce-specific configuration
Configuring payment handling

135

Conﬁguring payment logging

Payment handling logging is turned off by default. You can turn it on by modifying the
$bv1TO1_VAR/etc/.bvlog.conf conﬁguration ﬁle. [See “.bvlog.conf” on page 184 for details.] To
turn payment handler logging on, add the following line to the conﬁguration ﬁle:

29

0:3

pmtlog% SHORT

// Send payment logs to pmtlog, short format

The line tells One-To-One to log payment transactions to
$BV1TO1_VAR/logs/hostname/pmtlog.YYMMDD; where hostname is the name of the host
machine, and YYMMDD is the date of the log ﬁle.

See “Conﬁguring microtransaction logging” on page 129 for information about microtransactions.

Conﬁguring Omnihost (Solaris only)

Omnihost is not available on the HP-UX and Windows NT platforms.

Omnihost is one of the payment handlers that One-To-One uses to process electronic credit card
purchases. When a purchase request occurs, Omnihost connects with a bank to get authorization for
the purchase. To identify your account to the bank, Omnihost uses the account information stored in
the omnihost.cfg database ﬁle in $BV1TO1/bin, as speciﬁed by the param_file parameter in
bv1to1.conf:

param_file=$env(BV1TO1)+”/bin/omnihost.cfg”

When you get your account from the bank, the bank provides most of the information that you need
to put in the ﬁle. However, you provide the information speciﬁc to your business, such as the
maximum purchase amount allowed. Following is a partial listing of the ﬁle, items in bold are ones
that you must provide; the other items are the information you get from the bank. The table that
follows the listing describes the customizable ﬁelds in detail.

[OMNIHOST]
HOSTNAME=Mercury
PORT=8012
SETTLE_BATCH_MAX_RECS=20
NUM_CONNECTIONS=2

[VISAF]
MAX_AMOUNT_FIELD_SIZE=7

[BATCHDEFAULTS]
MAX_AMOUNT=000009999999

[STORE_BEGIN]
STORE_NAME: BestBuyClothing

Installation and Administration Guide

BroadVision, Inc.

136

Chapter 7 Commerce-specific configuration
Configuring payment handling

[MERCHANT]
MERCHANT_NAME=BestBuyClothing, Inc.
CITY_NAME=Los Altos
STATE_NAME=CA

[TERMINAL]
TERMINAL_NUM=9997
TIMEZONEDIFF=248
TERMINAL_ID=99999997
[STORE_END]

Field name

HOSTNAME

PORT

Contents

The name of the host machine that runs the Omnihost server.

The port ID number of the Omnihost server.

SETTLE_BATCH_MAX_RECS The number of records that can be settled in one batch transaction;
default is 20; the maximum is 50.

NUM_CONNECTIONS

The number of connections that can be made to the Omnihost server;
default is 2.

MAX_AMOUNT_FIELD_SIZE The count of digits, including two decimals, in the maximum authorized
purchase price. For example, a maximum size of 5 equates to 999.99; 7
equates to 99,999.99.

MAX_AMOUNT

The maximum authorized purchase amount. This is a twelve digit
number with leading zeros, and the last two digits represent the two
decimal digits. For example, for a maximum purchase of $1,750.75, use
000000175075.

BroadVision, Inc.

Installation and Administration Guide

8 Maintenance

137

Maintenance activities are a regular part of running a computer system. The activities in this chapter
reﬂect those that you are likely to perform while maintaining the BroadVision One-To-One
Enterprise, including:

l “Shutting down your site, next.

l “Restarting your site” on page 139.

l “Recovering after a crash” on page 140.

• “Backing up your site” on page 141.

• “Maintaining a stand-by server” on page 142.

• “One-To-One server machine crash” on page 143.

• “One-To-One unexpected behavior” on page 143.

• “Database server crash” on page 143.

• “Database corruption” on page 144.

• “Omnihost server machine crash” on page 144.

l “Monitoring server statistics” on page 145

l “Tuning for performance” on page 149

• Hardware conﬁguration, described on page 150.

• Tuning Interaction Managers, described on page 151.

• Tuning HTTP servers, described on page 152.

• Tuning One-To-One server processes, described on page 153.

l “Maintaining Interaction Managers” on page 154

• “Using Interaction Manager log ﬁles” on page 154

• “Monitoring for dead Interaction Manager servers” on page 155

l “Purging discussion group messages” on page 156

l “Determining software versions” on page 156

Installation and Administration Guide

BroadVision, Inc.

138

Chapter 8 Maintenance
Shutting down your site

Shutting down your site

It is important that when you shutdown a One-To-One site, that you do gracefully stop all
One-To-One processes and servers. Do that by following the instructions in this section.

To shut your site down:

1. Shut down all active One-To-One Command Center sessions, and any applications that are

clients of One-To-One. If you are running bvconf monitor, shut it down too.

2. Shut down all running Interaction Managers on each machine that hosts an Interaction Manager.

imgr_conf -a stop -A appName

If you have multiple Interaction Managers running on a host, be sure to specify the installation
name (appName) of each. [See “Named applications” on page 104 for information about the names.]

If you have Interaction Managers running on multiple hosts, perform the shutdowns on each
host machine by running imgr_conf while logged into the machines.

rlogin remoteHost
source $BV1TO1/VAR/etc/bv1to1.csh
imgr_conf -a stop -A appName

3. Shut down the connections from the existing business system (back end).

4. Shut down any processes that call One-To-One APIS, such as cron jobs that launch One-To-One

processes or database house cleaning activities.

5. From the root host, shut down the One-To-One servers. [See “shutdown” on page 181 for details

about bvconf shutdown.]

bvconf shutdown

The bvconf utility displays messages as it shuts down the system. When the system is
completely down, bvconf returns control to the command prompt. Wait for the command
prompt to ensure that everything has stopped before affecting the conﬁguration.

During this normal shutdown, some processes will complete the current jobs before allowing
bvconf to ﬁnish. This is especially true of Notiﬁcation servers that are generating visitor
messages. If you kill those processes before they ﬁnish, you risk sending multiple copies of
messages to the same recipients.

If the shut down reports any errors, manually kill the offending processes with bvconf
shutdown -f. [See “shutdown” on page 181 for details.] Also, check the log ﬁles to determine why
the process did not die gracefully and attempt to remedy the problem.

Once bvconf is ﬁnished with the shutdown, you can backup, alter, or edit the system.

BroadVision, Inc.

Installation and Administration Guide

Restarting your site

Chapter 8 Maintenance
Restarting your site

139

Restart your site while logged in with the account that conﬁgured One-To-One. Never start
One-To-One as the root user.

To restart your system after it has been shut down:

1. From the root host, restart the servers with bvconf:

• If you changed any of the conﬁguration settings use bvconf execute to enable the

changes. [See “execute” on page 175 for details about this process.]

 source $BV1TO1/VAR/etc/bv1to1.csh
 $BV1TO1/bin/bvconf execute

CAUTION That needs repeating! Source one of the configuration files before starting any of the
One-To-One or Interaction Manager servers, utilities, or scripts. This is one of the most
common mistakes and failing to do so causes problems starting the site.

• If you are restarting after recovering from a crash:

$BV1TO1/bin/bvconf execute

• If you made no changes to the conﬁguration, use bvconf restart. [See “restart” on

page 181 for details about this process.]

$BV1TO1/bin/bvconf restart

When bvconf returns control to the command prompt, the One-To-One servers have been
launched. However, some servers will not appear to be active until a request is made of them.

2. Reconnect the existing business system.

3. Restart the Interaction Manager servers by running imgr_conf on the machines that host the
Interaction Manager servers. If you have multiple Interaction Managers, be sure to also specify
the installation name (appname) of each. [See “Conﬁguring and starting the Interaction Manager” on
page 40 for details about starting the manager.]

$BV1TO1/bin/imgr_conf -a start [ -A appName ]

The imgr_conf utility returns control to the command prompt after the Interaction Manager
servers have been launched. However, the servers are not completely restarted until they
display the “version” message in the terminal window where you ran imgr_conf. Each
Interaction Manager engine generates the version message, which identiﬁes the engine and the
One-To-One version number, similar to this:

***bvsmgr/www.bvsn.com/.../BV_SessionManager0 OneToOne version: 4.0***

Make sure that the HTTP servers are running. If you changed the Interaction Manager
conﬁguration, stop and then restart the HTTP servers.

Once the Interaction Manager version message appears, visitors may use the site.

Installation and Administration Guide

BroadVision, Inc.

140

Chapter 8 Maintenance
Recovering after a crash

Recovering after a crash

If you have a system or machine crash, or if the data ﬁles become corrupt, you need to restore the
system to a good state. This section describes how to recover from some disasters, including:

l “Backing up your site” on page 141.

l “Maintaining a stand-by server” on page 142.

l “One-To-One server machine crash” on page 143.

l “One-To-One unexpected behavior” on page 143.

l “Database server crash” on page 143.

l “Database corruption” on page 144.

l “Omnihost server machine crash” on page 144.

The most important step to recovering after a crash is to prepare for the event. If you are careful
about how you configure, maintain, and back up your site, you should be able to restore all
information in the database up to the point of the crash, within the limitation of the database
management system.

If the database connection is ever lost, stop and restart all of the One-To-One database accessor
servers before continuing.

What follows are some general topics that you should be aware of regarding crash recovery.

Separate
database server
machines

One-To-One stores its critical data in a relational database. It uses the database in the standard way,
allowing it to exploit the strength provided by database vendors (such as distribution, robustness,
and scalability). As such, you can operate a separate database for your One-To-One activities, or use
an MIS-managed database running on separate machines. Whichever setup you use, for
performance reasons, you should run the database server on a machine separate from the
One-To-One server hosts. This conﬁguration also helps recover quickly in the event of a One-To-One
server machine crash; you continue to use the same database if you move the One-To-One servers to
a new machine.

Back up
conﬁguration ﬁles

The system conﬁguration and administration ﬁles are not dynamic, and are stored the
$BV1TO1_VAR/etc and $BV1TO1_VAR/dbschema directories. You need to back up at least three
files from the etc directory: admindb, session_terms, and bv1to1.conf. These files are small,
change infrequently, and can be backed up when One-To-One is running. Also, if you have any
custom libraries in $BV1TO1_VAR/lib, back them up too. In the event of a crash, you can restore
your site conﬁguration with these ﬁles.

Stand-by server

If a One-To-One server machine crashes, follow the instructions in “One-To-One server machine
crash” on page 143. In the event of a crash of the root host you need to be able to bring your site back
up quickly, consider maintaining a stand-by server. [See “Maintaining a stand-by server” on page 142
for details.]

Notiﬁcation
messages

Log ﬁles

When notiﬁcation jobs terminate prematurely, such as due to a server crash or forced shutdown, the
corresponding job directories and messages remain and will be resent when the system restarts.
While the system is still down, you should examine the directories and move or remove unsent ﬁles.
[See “Maintenance” on page 72 for details.]

One-To-One and the Interaction Manager servers write message to the log ﬁles that might be useful
in determining why a One-To-One system crashed. If you suspect a server problem, consult the log
ﬁles and try to determine why the system crashed before restarting it.

BroadVision, Inc.

Installation and Administration Guide

Backing up your site

Chapter 8 Maintenance
Recovering after a crash

141

When backing up your One-To-One site, you must maintain both the conﬁguration, and the state of
the databases. To accomplish this, shutdown the site and backup each of the following:

l The One-To-One database as identiﬁed by $BV_DB_DATABASE.

l The system configuration information stored in the $BV1TO1_VAR directory.

If your system suffers a data crash, you should be able restore all information in the database
file up to the point of the crash, within the limitation of the database management system.

To backup your system:

1. Backup the database per the procedures for your database management system. The database is

identiﬁed by $BV_DB_DATABASE.

2. Make a backup copy of all ﬁles in the $BV1TO1_VAR directory. These ﬁles contain the system
conﬁguration and administration information. You need to back up at least ﬁve ﬁles from that
directory: admindb, acldb, roledb, session_terms, and bv1to1.conf. These ﬁles are
small, change infrequently, and can be backed up when One-To-One is running.

• If you are maintaining a stand-by system, copy all the $BV1TO1_VAR/etc ﬁles to the

corresponding directory on the stand-by machine.

• This is a good time to merge observation log information into your observation database, if

you are tracking observation information.

• It is also a good time to truncate or cycle any log ﬁles that you want to keep for historical

purposes. All One-To-One log ﬁles are stored in $BV1TO1_VAR/logs. Additionally, if you
are using the AVP taxing program, you should truncate its log ﬁle. [See “Conﬁguring the
Taxing system” on page 126 for details.]

To truncate a log file ($BV1TO1_VAR/logs/logfilename) without shutting down the
servers, enter the following at a command prompt:

UNIX:

cat /dev/null > logfilename

Windows NT:

cat NUL: > logfilename

Note that some csh shells might require “>!” instead of just “>”.

3. Backup your database schema speciﬁcation ﬁles in the $BV1TO1_VAR/dbschema directory.

4. Truncate or purge your database transaction log ﬁles per the procedures for your database

management system.

5. If you are using a custom interactive application, backup any application state ﬁles.

6. Backup the existing business system state.

7. Restart your site per the instructions in “Restarting your site” on page 139. You can use the

bvconf restart process.

Notiﬁcation
system ﬁles

The Notiﬁcation system generates messages and might retain them in the $BV1TO1/messages
directory. If you want to backup the ﬁles in the messages directory tree, you need to shut down the
only the Notiﬁcation servers. [See “Conﬁguring visitor notiﬁcations” on page 69 for details.]

Installation and Administration Guide

BroadVision, Inc.

142

Chapter 8 Maintenance
Recovering after a crash

Maintaining a stand-by server

If the One-To-One root host machine crashes and you need the ability to bring the site back up
quickly, maintain a stand-by server. A stand-by server is a machine that is nearly identical to your
root-host machine’s conﬁguration. Both machines need to have the One-To-One software installed
and conﬁgured, though the stand-by machine does not need to have running software except when
it is being used as a replacement for the primary machine.

Preparing a
standby server

To prepare a stand-by server:

1. Install, conﬁgure, and start One-To-One on the primary machine per the instructions in Chapter

2, “Installation.” The last step in the start-up procedure is

bvconf execute -a install_all

2. After the system is running, shut down the primary system per “Shutting down your site” on

page 138. The important command is:

bvconf shutdown

3. Install One-To-One on the stand-by machine. Do not bother to conﬁgure or start the system on

that machine.

4. Copy all of the conﬁguration ﬁles from the $BV1TO1_VAR/etc directory on the primary

machine, to the $BV1TO1_VAR/etc directory on the stand-by machine.

5. Start and then stop the system on the stand-by machine:

bvconf execute
bvconf shutdown

6. Restart the primary machine.

bvconf restart

Your stand-by machine is now ready.

Maintaining a
standby server

Starting the
standby server

To keep your stand-by system up-to-date with the primary system, periodically copy the contents of
the $BV1TO1_VAR/etc directory into the $BV1TO1_VAR/etc directory on the stand-by machine.
At least copy these ﬁles session_terms, and bv1to1.conf. These ﬁles are small, change
infrequently, and can be backed up when One-To-One is running.

If the primary server crashes, switch to the stand-by server by:

1. Shut down the Interaction Managers per the instructions in “Shutting down your site” on

page 138.

2. Restart the system per the instructions in “Restarting your site” on page 139, run bvconf

restart on the stand-by setup when starting the host.

You might want to combine the One-To-One switch-over process with your network switch-over,
which can be done either by routers or DNS.

BroadVision, Inc.

Installation and Administration Guide

Chapter 8 Maintenance
Recovering after a crash

143

One-To-One server machine crash

If one of the machines hosting a One-To-One Service crashes

1. Shut down the site per “Shutting down your site” on page 138.

2. Try restarting the machine.

If you have to replace the crashed machine, and that machine is one of many hosts in the
One-To-One system, and that machine is not the one where you run bvconf, you must either:

• Give the new machine the same name as the old machine, or

• Change your bv1to1.conf conﬁguration ﬁle to replace all references to the old machine

with the new machine’s name.

3. When the machine is running, restart the site per “Restarting your site” on page 139.

One-To-One unexpected behavior

If One-To-One is behaving unexpectedly:

1. Shut down all the servers per “Shutting down your site” on page 138.

2. Make a copy of all the ﬁles and directories in $BV1TO1_VAR/logs for debugging purposes.

3. Restart the servers per “Restarting your site” on page 139.

The bvconf execute process checks and restores the system management state to a consistent
state. If you have problems with the One-To-One system, try running this process.

If the problem continues, contact BroadVision immediately. Be sure to maintain any server core ﬁles
in $BV1TO1_VAR/logs/<host name>/.

One of the most common causes of unexpected behavior comes from running One-To-One
utilities or scripts in a terminal that does not have the correct One-To-One environment variable
settings. Always source the environment variables from one of the scripts described in “Shell start-
up scripts” on page 39 before running One-To-One utilities or scripts.

Database server crash

If a database server crashes, Interaction Manager will keep retrying any database access activities.
However, the connection to the database will be lost and you need to shutdown and restart the
One-To-One servers per “Shutting down your site” on page 138 and “Restarting your site” on
page 139.

Installation and Administration Guide

BroadVision, Inc.

144

Chapter 8 Maintenance
Recovering after a crash

Database corruption

If any of the database ﬁles have become corrupt (such as when the database recovery doesn’t work),
you must restore all ﬁles to the previous backup (described in “Backing up your site” on page 141).

To recover after a database crash:

1. Shut down the site per “Shutting down your site” on page 138.

2. Reboot all machines and wait for them to settle (no running httpd, applications, or such).

3. Make a copy of all the ﬁles and directories in $BV1TO1_VAR/logs/ for debugging purposes.

4. Make a snapshot backup of the databases for debugging and data recovery.

5. Roll back and restore the database identiﬁed by $BV_DB_DATABASE.

6. Restore the conﬁguration and administration information ﬁles backed up from the

$BV1TO1_VAR/etc directory.

7. If you are using an interactive application, restore the application state ﬁles.

8. Restore the existing business system state.

9. Restart the servers per “Restarting your site” on page 139.

Omnihost server machine crash

If you are using the Omnihost Payment Handler and that server’s machine crashes such that you
need to replace the machine:

1. Shut down all the servers per “Shutting down your site” on page 138.

2. Replace the machine and software.

3. Change the Omnihost conﬁguration ﬁle to reﬂect the new conﬁguration. [See “Conﬁguring

Omnihost (Solaris only)” on page 135 for information about the ﬁle.]

4. Restart the servers per “Restarting your site” on page 139.

BroadVision, Inc.

Installation and Administration Guide

Chapter 8 Maintenance
Monitoring server statistics

145

Monitoring server statistics

Many of the One-To-One servers track and publish statistics about their performance, including
general information about memory footprint, CPU usage, count of IDL requests in the queue, and
server boot up time. They can also track information speciﬁc to their task: the database accessor
tracks the count of SQL queries made and their response time; the name server counts how many
name resolution requests it processed; the administration server tracks the count of logins.

To monitor server statistics, use the monitor process of the bvconf utility. This process runs in a
terminal window and has three modes of operation: report, interactive, and explore. That later two
modes are used mainly for debugging and testing CORBA servers, and are not discussed here. For
detailed information about the monitor process, see “monitor” on page 177.

You must stop monitor before you shut down servers that you are monitoring, or unexpected
results will almost certainly occur.

Report mode

The report mode, also known as the “top” mode, displays selected statistics from a set of servers.
The display is refreshed periodically — much like the UNIX top command. The report mode is
activated by specifying one of the -a, -p, or -u options. For example, to see the statistics for all
monitorable processes (except Interaction Manager) running on all host machines in the
One-To-One conﬁguration, use -a:

bvconf monitor -a

By default, the display updates every 10 seconds (a rate that you can change the with -s option).
Use ^C to stop the monitoring and return to the command line.

Process

Host

Distributed memory block

Time of last update

Specific statistic

Standard statistics

Processes do not appear in the display until they have been started, which usually doesn’t happen
until the server receives its ﬁrst request for information. To launch all the processes that are
conﬁgured for the site, use the -l (lowercase ‘L’) option.

If you stop and then restart servers, stop and restart the monitor before restarting the server.

Installation and Administration Guide

BroadVision, Inc.

146

Chapter 8 Maintenance
Monitoring server statistics

Statistics

Each row of statistics describes the information for one process running in the system. The row
begins with information that identiﬁes the process, is followed by standard statistics, and ﬁnishes
with any statistics that are speciﬁc to the task, such as the count of logins in the example above.

Column

Description

HOST

ID

GROUP

STIME

IDLQ

VSZ

RSS

CPU

LWP

USR

SYS

Host machine running the process.

Instance of the process (of which multiple can be conﬁgured in the bv1to1.conf ﬁle), or
engine ID of the Interaction Manager.

Process group (which is deﬁned in the bv1to1.conf ﬁle), or Interaction Manager application
name.

Start time of server. The start times should be relatively close. Later times might be an
indication that a server crashed and was automatically restarted.

Total count of IDL requests queued up in the Interaction Manager — these are requests to
evict or refresh information from the cache.

Virtual memory size of server process (in Kilobytes). If a process is growing in size, it
probably has a memory leak. If it is an Interaction Manager process (see below), the culprit
is most likely a component or dynamic object. Though Interaction Manager servers do
grow and shrink — from garbage collection — during normal use.

Resident memory size of server process (in Kilobytes).

CPU percentage consumed by this process. If a process is using most of the CPU time,
consider moving it to another host, or creating an additional process, possibly running on
another machine. Both of these speciﬁcations are done in the bv1to1.conf ﬁle.

Windows NT: The CPU % reported is against a single processor. If a server is taking up a
whole CPU on a 4 processor machine, this statistic will report 100%, while the
Windows NT Task Manager will report 25%. The value reported by this statistic is
consistent with “% Processor Time” on the Windows NT Performance Monitor.

Number of light-weight processes (threads).

Accumulated user mode CPU time (seconds).

Accumulated system mode CPU time (seconds).

Process names

To monitor a speciﬁc process, use the -p mode and specify the process to watch. For example, to
monitor the cntdb (content database accessor) process on the current host machine:

bvconf monitor -p cntdb

To determine a process name, use the -a option to see all processes, or when a server is running,
you can ﬁnd its process name from the list generated by bvconf ps. For example, here are three
server processes:

UNIQPID
p_1221_4
p_1221_1
p_1221_3

EXEC

TYPE
objsrv cntdb
objsrv bvconf_srv
objsrv cmsdb

HOST
adrastea
adrastea
adrastea

PORT
1303
1301
1307

PID
1785
1656
1890

Two of these processes are conﬁgurable and are deﬁned in the bv1to1.conf ﬁle:

process cntdb {}
process cntdb {}

# 1st instance
# 2nd instance (can have more)

BroadVision, Inc.

Installation and Administration Guide

Database
accessor statistics

The database accessor processes have additional statistics available from the BV_DB_STAT memory
block. These statistics provide information about database accesses, including the count of selects,
updates, inserts, deletes, and stored procedure executions.

Statistics for the BV_DB_STAT
distributed memory object.

Content database statistics

Chapter 8 Maintenance
Monitoring server statistics

147

To see the database access statistics, include a -m BV_DB_STAT argument, like this:

bvconf monitor -p cntdb -m BV_DB_STAT

If you see an accessor hitting the database at a high rate and your application doesn’t make special
calls to cause that, the problem is probably with the cache. Try changing the cache size per the
instructions in “Conﬁguring caching” on page 58.

Interaction
Manager

To monitor the Interaction Manager processes, specify “bvsmgr” as the process name.

bvconf monitor -p bvsmgr

The display for Interaction Manager processes includes information about the current count of
sessions, connections, IDL requests, threads in use, and count of CGI requests processed.

Three Interaction Managers with
the default application name.

Interaction Manager statistics

When monitoring Interaction Manager processes, look for engines whose session count (SESS)
is zero (0), or whose session count is considerably fewer than the other engines. Such a process
might need to be restarted. Note that the connection manager between the gateway and the
Interaction Manager notices engines that are not responding and routes subsequent requests to
other engines.

You can limit the statistics to display by including the -L option and listing the columns to include,
for example:

bvconf monitor -L SESS,CONN,IDLQ,THR,CGI -p bvsmgr

The Interaction Manager display uses the “default” application. To monitor a speciﬁc named
application, use the -A option followed by the name. Optionally you can use an asterisk (*) to see all
applications in the site:

bvconf monitor -A * -p bvsmgr

Installation and Administration Guide

BroadVision, Inc.

148

Chapter 8 Maintenance
Monitoring server statistics

You can also watch a speciﬁc Interaction Manager engine by using -E to identify the engine number.
For example, to watch the second engine in the ﬁgure above, specify 1:

bvconf monitor -E 1 -p bvsmgr

Report options

Several options affect the report display. Here are a few of the notable ones:

-A appName

-C

-D | -R

A speciﬁc Interaction Manager named application.

Turn off full-screen display and scroll the report in the terminal
window. This is useful when you want to compare values between
multiple updates, or to redirect the output to a ﬁle. By default, the
report clears the screen before refreshing the display.

Report that delta (-D) or rate (-R) of change from the last update. By
default, the statistics track the total usage or “value”.

-E engineID

A speciﬁc Interaction Manager engine.

-h hostName | -H

A speciﬁc host (-h) or all hosts (-H).

-i instanceName

A speciﬁc One-To-One server instance. Not available on all
platforms.

-l

Include inactive servers.

-L label[:mode]

[,label[:mode] …]

-m memoryName | -M

-n count

-p processName

-s seconds

-U

-w characters

Show just the named statistics for the processes being reported.
Optionally, you can identify the mode for each a D (delta), R (rate of
change), or V (total value). The default mode is value. If you omit -L,
the report includes all statistics.

Here’s an example that uses all three modes:
-L CPU:D,USR:V,RSS:R

A speciﬁc memory object (-m) or all memory objects appropriate for
the context (-M). The default if you omit this option is
BV_SRV_STAT.)

Show and update the report <count> times and then quit. By
default, the report updates continuously until you stop it with ^C.

A speciﬁc process. For default Interaction Manager applications, use
“bvsmgr”.

Interval (seconds) between report updates. The default rate is 10
seconds.

Show unlabeled values too.

Width of the report in the terminal window. By default, the report tries
to ﬁll the width of the terminal window.

BroadVision, Inc.

Installation and Administration Guide

Tuning for performance

Chapter 8 Maintenance
Tuning for performance

149

One performance goal for a One-To-One Web site is to optimize the dynamic page throughput —
dynamically generating and producing the page that the visitor sees. To achieve this goal,
One-To-One supports load balancing by providing ﬂexible conﬁgurations in that it can run on
multiple machines and its processes can have multiple instances. There are also many parameters,
such as cache sizes, that you can tune, although the default conﬁguration works out-of-box.

Tuning a site for performance is not a simple formula or spreadsheet for choosing parameters,
because work load is application and site dependent. This discussion, therefore, is a guideline that
describes the parameters and conﬁgurations that you can adjust, and how to adjust them. It does
not, however, address day-to-day operation and conﬁguration procedures. Those topics are covered
elsewhere in this manual.

At any site, to achieve high throughput, you need to be careful about your application code.
Avoid long blocking routines, I/O activities, and database accesses. If your application has a
heavy dependency on external data, try to cache the data.

The One-To-One software is designed to run on multiple machines. For purposes of this discussion:

l Interaction Manager machines host the Interaction Manager servers. These may be on the same

machine as the HTTP server, but are usually separate, and behind a ﬁrewall. For speciﬁc tuning
instructions, see “Tuning Interaction Managers” on page 151.

l Front-end machines host HTTP servers. For speciﬁc tuning instructions, see “Tuning HTTP

servers” on page 152.

l Back-end machines run One-To-One servers, and do not host HTTP daemons or Interaction
Manager servers. Machines may run One-To-One servers, HTTP daemons, and Interaction
Manager servers. For speciﬁc tuning instructions, see “Tuning One-To-One server processes” on
page 153.

To tune a site, you monitor the activities of the various processes and machines to identify the areas
that are blocking throughput. In particular, you want to ensure that your machines are not
unwillingly blocked when there is work to be done. You also want to avoid too much idle time,
which represents unnecessary capital investments.

Symptoms and
remedies

Here are some common symptoms and activities that improve performance:

l Identify CPU-intensive processes.

• If all your existing machines have reached close to 100% CPU utilization and you have not

achieved your throughput goal, add more machines. See “Hardware conﬁguration,”
described next.

• If you are running One-To-One servers and Interaction Manager servers on the same

machine, and the CPU usage is close to 100% and you want more thoughput, separate the
servers to different machines.

• If a back-end machine reaches close to 100%, off-load some of the One-To-One servers to
another machine. In particular, the database accessor processes, cntdb and cmsdb,
consume lots of CPU time. [See “Tuning One-To-One server processes” on page 153.]

• If you see high CPU utilization of the cntdb process (Content database), try increasing the
content database cache as speciﬁed in “Conﬁguring caching” on page 58. If a bigger size
does not reduce the load, add more instances of the cntdb database access process. You
should see an immediate improvement. To determine the optimal count of processes, keep
adding them until you do not see a reduction in CPU utilization.

Installation and Administration Guide

BroadVision, Inc.

150

Chapter 8 Maintenance
Tuning for performance

l If your CPU utilization is low and your browsers see long latencies, you probably have network

problems. There are two common possibilities.

• If browsers see long latencies in getting a connection, you probably do not have enough

HTTP servers. [See “Tuning HTTP servers” on page 152.]

• If browsers see slow transfer rates, you probably do not have enough external network

bandwidth.

If adding HTTPD and increasing external network bandwidth do not improve the situation,
you need to tune other parameters.

Network

For you internal network, connect the HTTP, Interaction Manager, and One-To-One host machines
to a LAN with at least 100 Mb Ethernet.

For your external network, estimate the amount of data your need to transfer, including the number
hits per second, size of a hit, amount of graphics, and other network activities. You see extremely
poor network latencies if you overload your external network feed, such running your e-mail server
for targeted e-mails through the same network connection as your HTTP servers. Periodically run
ping from your internal server machine to an outside machine to monitor the health of your
external network during peak hours.

Hardware conﬁguration

The hardware that you need depends mainly on your work load. One-To-One has a scalable
architecture that can exploit multiple machines, allowing you to add more machines over time as
your work load grows. Instead of buying a huge machine to meet your ultimate future needs, you
can start with smaller machines. This modular approach gives you a smooth upgrade path. It also
avoids hitting the scalability limit of the underlying operating system, by using multiple operating
systems on multiple machines.

Grow your hardware in incremental steps based on your work load requirements. If your steps are
too small, you end up with too many machines, which makes conﬁguration and system
management complex. On the other hand, if your steps are too big, you experience large quantum
jumps in your growth path and spend more than you have to at the beginning.

How many
machines

Roughly, you need one high-power front-end machine (a host running HTTP servers and
Interaction Managers) to handle 1 to 2 million dynamic hits per day, assuming steady load 24 hours
a day. If you have heavier trafﬁc, you need more machines. HTTP servers, being the network
connection points, usually run outside of the ﬁrewall.

A well tuned Interaction Manager server machine is CPU-bound.

For security reasons, most sites prefer to put all back-end and Interaction Manager machines behind
the ﬁrewall; machines different from those running the HTTP servers. On the back-end, you need
about one half or one third of the number of front-end boxes. Add more machines if all your existing
machines have reached close to 100% CPU utilization and you still have not achieved your
throughput goal.

If, however, you are not getting the throughput you want, and your machines are idling, do not add
more machines. Consider adjusting the number of HTTP servers in use on your front-end machines.
[See “Tuning Interaction Managers” on page 151 for more information.]

BroadVision, Inc.

Installation and Administration Guide

Solaris machine conﬁgurations

Chapter 8 Maintenance
Tuning for performance

151

To give you an idea of the range of conﬁgurations the One-To-One runs on, at BroadVision, for some
internal testing, such as internationalization, we adequately run the whole system (HTTP,
Interaction Manager, and One-To-One servers) one a single 64MB 85MHz Sparc 5. However, we
perform stress testing using multiple 8 processor, 243 MHz, E4000 machines. Some heavily leaden
customer sites use 24 Ultra CPUs across three machines. We do not see scalability limits in these
conﬁgurations and expect to be able to exploit even more CPUs.

Here are the main points to consider:

l Machines — For a small site, a single 2 processor Ultra is a good building block. For a large site,

use a larger box as building blocks to avoid having too many little machines.

l Memory — Use 64 to 128 MB main memory per CPU. Watch virtual memory behavior (vmstat).

If you see high paging, increase main memory.

l Swap space — Have sufﬁcient swap space: at least twice the amount of main memory. For a
good discussion about swap space, see the Netscape knowledge article on swap space,
“Conﬁguring swap space for your Enterprise Server”, issue # 970513-7.

If you see excessive swapping, as monitored with the Solaris vmstat 1 command and options,
add more main memory. A well-balanced system should see little swapping.

Operating system Apply all relevant kernel patches. A high-trafﬁc web site stresses the kernel a lot! Watch for patches

that ﬁx hangs, race conditions, and fork problems. Also, tune the operating system networking
options. For some good discussions, see the Netscape knowledge articles on TCP/IP: “How to Tune
Solaris for Enterprise Server Performance”, issue #970815-12, and “Enterprise Server in SSL 3 mode
and doing KeepAlive connections/Netscape Browsers”, issue #80226-1.

Solaris-speciﬁc
tools

Some of the tools that are useful for monitoring processes and machine include these Solaris and
UNIX monitoring tools:

l Use the UNIX swap utility with its -l and -s options to ensure that you have sufﬁcient swap

space.

l Use the UNIX perfmeter utility to watch CPU load and packet rate. It graphically shows some

of the same information that the UNIX vmstat 1 provides.

l Use the UNIX top utility to identify CPU-intensive processes.

Tuning Interaction Managers

The Interaction Manager servers can run on their own host machines, separate from the HTTP and
One-To-One server machines. Additionally, each host can run multiple instances of the server: each
instance is called an engine. Best Interaction Manager performance is usually attained with two to
four engines per processor (on an Ultra machine). Having too many Interaction Managers — more
than 4 per processor — typically does not help.

On a development site, you can run multiple, independent Interaction Manager servers on a
single machine, just don’t expect high throughput.

You probably need more Interaction Manager engines if

l you have not reached your throughput goal, and

l all your Interaction Managers consume heavy CPU time, and

l you still have lots of idle CPU time on your front-end (HTTP server) machines.

Installation and Administration Guide

BroadVision, Inc.

152

Chapter 8 Maintenance
Tuning for performance

If you saturate the CPU of a Interaction Manager machine and you need more throughput, consider
adding more Interaction Manager machines. A single tuned HTTP server [see “Tuning HTTP servers”
on page 152] can drive multiple Interaction Manager engines across multiple machines, which in
turn access a single One-To-One server machine.

On a well tuned One-To-One system, the Interaction Manager machines are CPU-bound.

If your Interaction Manager machines are not CPU bound and you are seeing long delays or low
throughput, look to see if your application operations have long block times. If this is the case, you
should execute the long-block operations in the Interaction Manager’s “parallel mode” (see the
Developer’s Guide to Components and Scripts for details). If you use parallel mode, increase the number
of Interaction Manager worker threads, the default is 16 per engine.

However, if the HTTP server is the bottleneck, consider running multiple HTTP servers on one or
more front-end machines. Multiple HTTP servers sharing the same domain name, such as with a
Cisco local director, can talk to the multiple Interaction Manager engines as long as the site has a
common setup. [See “Ports and IP addresses” on page 108.]

The biggest cause of the HTTP server being the bottleneck is lots of static ﬁle requests, especially
graphics, that need to be retrieved from the HTTP server’s document root directory. Each request for
a graphic is handled by a thread, which can be limited by the ﬁle descriptor conﬁguration for the
machine. See the next section, “Tuning HTTP servers, for ideas about improving this.

Tuning HTTP servers

You can run multiple HTTP daemons on a machine. The total number of HTTP connections that a
machine can support is the number of daemons times the maximum count of threads per daemon.
An Ultra 2 can comfortably run 4 to 64 daemons. Having more than you need only wastes swap
space. However, if you have too many, you might hit kernel limits, like the maximum number of
open ﬁle descriptors.

For best HTTP performance with One-To-One, use Netscape Enterprise Server or Microsoft
Internet Information Server (IIS), do not use Standard CGI.

The biggest cause of the HTTP server being the bottleneck is lots of static ﬁle requests, especially
graphics, that need to be retrieved from the HTTP server’s document root directory. Each request for
a graphic is handled by a thread, which is limited by the ﬁle descriptors for the machine.

Netscape Enterprise Server

If you are using the Netscape Enterprise Server, you generally want to use the most recent release
with the relevant patches installed. These notes apply to Netscape Enterprise Server 3.5.1, plus
patches through E.

Small to medium
load

Enterprise Server 3.5.1 is good for small to medium sites. It is not suitable for a extremely large site
because of its single-process architecture. A 3.5.1 site uses only one HTTPD process (with multiple
threads in it). Additionally, the HTTP process has a hard limit of 1024 open ﬁle descriptors, which
sets a cap on the maximum number of browsers that can talk to your site concurrently because each
concurrent connection takes one or more ﬁle descriptors. (You can ease this problem by having
multiple logical HTTP sites, each with a limit of 1024 open ﬁles.)

BroadVision, Inc.

Installation and Administration Guide

Chapter 8 Maintenance
Tuning for performance

153

Heavy load

Some One-To-One sites need to support a huge number of concurrent connections. In this case
Netscape Enterprise Server 2.0.1, with its multiple-process architecture, is a better choice. Two
Netscape conﬁguration parameters, in magnus.conf, are especially useful for tuning:

l MaxProcs — the maximum count of processes

l MaxThreads — the maximum count of thread

The product of these two parameters is the maximum number of connections your site can support.
For example, if you specify 100 processes with 24 threads each, you get 2400 concurrent connections.
In this example, you avoid the open ﬁle limit because each process has only 24 threads. Don’t set the
number of threads per process too high: 16 is a good starting number. Raise the value if you need more;
lower it to improve stability. The idea is to balance the number of threads per process with the
number of processes.

Tuning One-To-One server processes

One-To-One employs many types of back-end servers or daemons, all of which are conﬁgured with
settings in the bv1to1.conf conﬁguration ﬁle. The ones that can beneﬁt from having multiple
instances are:

l the database accessor processes cntdb, cmsdb, extdbacc, and genericdb.

l the Notiﬁcation servers sched_srv and alert_srv. See “Processes and daemons” on page 74

for complete information about conﬁguring and tuning these processes.

l the payment handler process pmthdlr_d. In most situations, the default conﬁguration settings
for pmthdlr_d work ﬁne [see “Conﬁguring payment daemons” on page 132 for more information].
However, you can group services into clusters and have a separate set of order management
processes for each cluster. This mechanism is for sites with a large number of services and heavy
order processing. See “group” on page 172 for information about clustering.

You probably only need to adjust the database accessors.

Database
accessors

There are two ways to monitor database accessors to identify which, if any, need to be tuned:

l Watch their CPU utilization with the UNIX top command. A consistently high usage might

indicate a server that needs more instances.

l Use bvconf monitor -m BV_DB_STAT -a [see “Monitoring server statistics” on page 145] to

watch the database query rates of an accessor. A database accessor is highly loaded if it
consumes lots of CPU time or if it has high query rates.

To tune your database accessors, use any or all of these techniques:

l Change the count of accessor instances. Increasing the count of database accessor process
instances provides multiple concurrent database connections. You need more of them if

• you have not reached your throughput goal, and

• the Interaction Manager machines still have lots of idle CPU time, and

• the cmsdb (Visitor proﬁles) or cntdb (Content) process consumes lots of CPU time.

See “Conﬁguring database accessors” on page 66 for information about adding processes. The
optimal count varies from application to application.

Each Interaction Manager engine uses just one database accessor, which is randomly assigned
when the engine starts. To take advantage of multiple database accessors, you need to have at
least as many Interaction Manager engines. See “Configuring the Interaction Manager server”
on page 40 for information about setting the count of processes per named application.

Installation and Administration Guide

BroadVision, Inc.

154

Chapter 8 Maintenance
Maintaining Interaction Managers

l Place the instances on different machines. When all of the CPUs on a machine are heavily

loaded, move some or all of the database accessors another machine. Use the process’s host
parameter to identify the machine. [See “Deﬁning processes” on page 67.]

l Tune cache parameters. Increase the size of the database cache to reduce query rates. [See

“Conﬁguring caching” on page 58.] For standard One-To-One functions, you should see low
database query rates if you have well tuned cache parameters.

Finally, review your application to see if you can avoid doing unnecessary database operations.
Especially watch out for complex SQL queries that require multiple requests of the database.

Maintaining Interaction Managers

Most of the instructions for conﬁguring and maintaining Interaction Manager servers are described
elsewhere in this manual:

l To conﬁgure your Interaction Managers, see “Conﬁguring the Interaction Manager server” on

page 40.

l To start or stop the Interaction Managers in your site, see “Restarting your site” on page 139 and

“Shutting down your site” on page 138.

l For speciﬁc information about starting and stopping a single, Interaction Manager server, see

“imgr_conf” on page 194.

If you are having problems with Interaction Managers in your site, see:

l “Using Interaction Manager log ﬁles,” described next.

l “Monitoring for dead Interaction Manager servers” on page 155

l “Troubleshooting Interaction Manager start-up problems” on page 49.

Using Interaction Manager log ﬁles

The HTTP server and Interaction Manager servers write errors to log ﬁles. Most of the log ﬁles are
written into subdirectories in the /tmp directory on the host machine. Additionally, when the
Interaction Manager is running, it writes errors and messages to the $BV1TO1_VAR/logs/
directory. If the ﬁles or directory doesn’t exist doesn’t exist when an error occurs, the system creates
it.

Location

/tmp/BVSNcgi_logs/*

/tmp/BVSNsmgr_logs/*

Messages

Communication errors.

Conﬁguration errors.

$BV1TO1_VAR/logs/<host name>/bvobs.out.YYYYMMDD

Messages and errors.

$BV1TO1_VAR/logs/<host name>/orbix.log

Orbix connection errors.

If you don’t want the files to consume swap space in your /tmp directory, make the directory a
symbolic link to a different file system before starting the Interaction Manager.

BroadVision, Inc.

Installation and Administration Guide

Chapter 8 Maintenance
Maintaining Interaction Managers

155

The log ﬁle names are descriptive of the system that generate the error. Additionally, when the name
contains a numeral, such as “bvsmgr_1.cfg”, it identiﬁes the messages coming from a speciﬁc
Interaction Manager engine. Here are some examples of typical log ﬁles:

Log ﬁle name

[<App>_]nsapi.log

[<App>_]cgi.log

Example

Contains runtime errors for …

foo_nsapi.log

Netscape Enterprise Server runtime errors

foo_cgi.log

CGI runtime errors

[<App>_]bvsmgr_<eng_id>.cfg

bvsmgr_0.cfg

Interaction Manager conﬁguration.

bvsm.startup.log

bvsm.startup.log

imgr_conf runtime errors

bvobs.out log ﬁle
messages

The log ﬁle entries in the bvobs.out ﬁle begin with the process and thread ID values, in square
brackets ([]), followed by the time of the event, the logging level (such as DEBUG), and a message
that describes the event. In the following example, the ﬁrst line is a CGI log entry, which does not
have a thread ID, and the second line is an NSAPI log entry:

[3827] Thu Aug
[13387 - 415816] Thu Aug

6 13:09:06 1998 [DEBUG] send successfully

6 13:53:57 1998 [DEBUG] msgXfer: receive OK

The cgi-log-level setting in bvsm.cfg determines the logging level. This is deﬁned by
imgr_conf -a configure.

Monitoring for dead Interaction Manager servers

The watcher utility allows you to monitor the state of your Interaction Managers, and restart any
that are found to be not running. You can monitor the default installation by running watcher with
no command-line arguments:

watcher

Or, to watch another installation, use the -a option and specify the installation’s application name:

watcher -a appname

The watcher utility checks for expired Interaction Managers at a frequency deﬁned in the
Interaction Manager conﬁguration ﬁle, which you edit by running imgr_conf -a configure.

Launch this program from the user account that launched Interaction Managers. Additionally, it
must be run with the same environment used to install and start Interaction Managers. The safest
way to do this is to source the appropriate shell script, $BV1TO1_VAR/etc/bv1to1.conf.csh or
…/bv1to1.conf.sh, before launching the program [see the “Shell start-up scripts” on page 39].

Once started, watcher will run until it is explicitly killed. To stop watcher, you need to ﬁnd out its
pid and kill it manually. Also, any automated shutdown/startup scripts should also include
watcher. Do not run more than one instance of watcher because that can cause race conditions when
they all try to restart a downed Interaction Manager.

The watcher program logs information about when Interaction Manager engines were checked,
and if it tried to restart them. This information is written to the general bvlog ﬁle. See “.bvlog.conf”
on page 184 for details about logging.

Installation and Administration Guide

BroadVision, Inc.

156

Chapter 8 Maintenance
Purging discussion group messages

Purging discussion group messages

To remove messages from the discussion group database, use the purge_messages.sql script.
You can ﬁnd this script in the $BV1TO1/bin/scripts/ directory. For information about running
this script, see the Database Administrator’s Guide.

Determining software versions

While the One-To-One system is running, you can determine the version of the release.

l To learn the server version, run bvconf and request the 1to1_version value. Identify your
site’s name, as speciﬁed in the site speciﬁcation in your bv1to1.conf conﬁguration ﬁle:

bvconf get_param siteName 1to1_version

Or, you can use the “@my-site” reserved name:

bvconf get_param @my-site 1to1_version

l To learn the Interaction Manager’s version, run bvsm_version, it takes no arguments:

bvsm_version

You can determine which, if any, software patches are installed by looking at the ﬁles in the
$BV1TO1/versions/ directory.

BroadVision, Inc.

Installation and Administration Guide

9 Utilities and other files

157

There are several utilities and conﬁguration ﬁles that you use when installing and conﬁguring
One-To-One. The previous chapter shows you how to quickly use the scripts, utilities, and ﬁles; this
chapter describes each in greater detail.

Utilities and scripts Use the utilities and scripts when initializing and conﬁguring One-To-One.

• “acltool” on page 158

• “cache_utl” on page 191

• “migr_coll” on page 197

• “bounced_email_utl” on page 160 • “dump_taxon” on page 193

• “migrate_to_v3.0” on page 198

• “bvconf” on page 174

• “imgr_acltool” on page 193

• “migrate_to_v4.0” on page 198

• “bvkill” on page 183

• “bvlog” on page 183

• “imgr_conf” on page 194

• “migrate_to_v4.1” on page 198

• “indexer” on page 195

• “tmpl_mgr” on page 198

• “bvping” on page 188

• “load_data” on page 197

• “watcher” on page 200

• “bvsm_version” on page 191

One Windows NT, run these commands in an MKS shell.

Conﬁguration ﬁles One-To-One uses the following ﬁles to determine conﬁguration settings.

• “.bvlog.conf” on page 184

• bvobs.conf

• “bvsm.cfg” on page 190

• “bv1to1.conf” on page 161

• “bvsm.ACL” on page 189

• “bvsm.req” on page 191

Database speciﬁc Many utilities and scripts are for use with the database and are described in the Database

Administrator’s Guide, including the following:

•apply_sql

•load_v2cnt

•purge_messages

•bv_load_content

•map_store_user

•purge_agg_obs

•bv_load_users

•mxt_load

•purge_raw_obs

•install_observe_db

•obs_dbload

•sch_gen

•load_v2cat

•obs_aggr

Developer
speciﬁc

For information about these utilities, see the Developer’s Guide to Components and Scripts:

•ctxdriver

•jsic

Installation and Administration Guide

BroadVision, Inc.

158

Chapter 9 Utilities and other files
acltool

acltool

Reports the access control speciﬁcations for an access control ﬁle. Can be run interactively or
speciﬁcally.

Syntax

acltool [-f aclfile]

[ command argumentList ]

-f aclﬁle

checkpermission options

help

listcs [subjectItem]

Identiﬁes an access control ﬁle to load. If you omit this option, you will
need to use the load command from the interactive prompt.

Checks the access rights for visitor classiﬁers for a speciﬁc subject and
subject item. Returns yes if the visitor classiﬁer has access permission;
otherwise, returns no. See the Usage section below for a description of
the options.

Lists the available commands.

Lists the access control speciﬁcations currently cached in the Access
Control manager. Include a subject_item to limit the list to just the ones
for that item. For example, to see all script speciﬁcations:

>listcs script

listpermissions options

Lists the access rights for speciﬁc visitor classiﬁers. See the Usage
section below for a description of the options.

load [aclFilePath]

Loads the control speciﬁcations from an ACL ﬁle and checks the ﬁle’s
syntax. If you omit aclFilePath, it loads the control ﬁle from the previous
load command, if any.

printplists subjectItem subject Lists the visitor classiﬁer speciﬁcations for a speciﬁc subject item. For

example:

>printplists broadway/scripts/registered/* script

returns

broadway/scripts/registered/* @guest-:@ALL+

quit

Exits the interactive mode.

Location

$BV1TO1/bin

Usage

To run this utility in interactive mode, omit the command argument when starting acltool.

Commands can be abbreviated to their least ambiguous spelling. For example, lo and loa are both
abbreviations for load, but list is ambiguous because it can be listcs or listpermissions.

The checkpermission command checks the access rights for visitor classiﬁers for a speciﬁc subject and
subject item.

checkpermission { [-user userName ]

|
[-curr_role currentRole ]
|
[-role_list usersRole ... ]  |
[-community communityName ]

}

-subject subjectItem -type subject [ -op operation ]

BroadVision, Inc.

Installation and Administration Guide

Chapter 9 Utilities and other files
acltool

159

You need to specify at least one of the visitor classiﬁers, and a subject and a subject_item. For
example, these commands check the permission of the @ALL and @guest visitor classiﬁers as
deﬁned in the Broadway sample ACL ﬁle:

acltool> load /etc/opt/BVSNsmgr/bvsm.ACL
acltool> checkpermission -user @ALL \

-subject broadway/scripts/registered/* -type script

yes

acltool> checkpermission -user @guest \

-subject broadway/scripts/registered/* -type script

no

The -op operation argument is for future use and not fully implemented at this time.

The listpermissions command lists the access rights for speciﬁc visitor classiﬁers on all subject item
patterns (of a certain type) stored in the ACL manager cache.

listpermissions { [-user userName ]

|
[-curr_role currentRole ]
|
[-role_list usersRole ... ]  |
[-community communityName ]

[ -type subject ]

[ -op operation ]

}

You need to specify at least one of the visitor classiﬁers. If you omit the -type options, acltool lists
the permissions for all subjects. For example, this command lists the script access permissions for
the member community as deﬁned in the Broadway sample ACL ﬁle:

acltool> listpermissions -community member -type script
script broadway/scripts/registered/* yes
script broadway/scripts/privileged/* no
script * yes

The -op operation argument is for future use and not fully implemented at this time.

See also

“imgr_acltool” on page 193.

Installation and Administration Guide

BroadVision, Inc.

160

Chapter 9 Utilities and other files
bounced_email_utl

bounced_email_utl

Sets the INVALID_EMAIL ﬂag in the BV_USER_PROFILE table for each visitor who’s e-mail
address appears in a speciﬁed ﬁle.

Syntax

bounced_email_utl filename

Location

$BV1TO1/bin

Usage

The ﬁle of e-mail addresses is a text ﬁle where the addresses are separated by a comma or space. The
e-mail address main contain alphanumeric characters, dashes (-), underscores (_), periods (.), and at
symbols (@). For example:

bvpubs@broadvision.com mgr@my_bank.com, mgr@best-buy-clothing.com

To generate the ﬁle from the “bounced” e-mail that your site receives, consider one of these third
party utilities listed in the One-To-One Server Release Notes.

See also

“Conﬁguring visitor notiﬁcations” on page 69 for information about e-mail notiﬁcations.

BroadVision, Inc.

Installation and Administration Guide

bv1to1.conf

Chapter 9 Utilities and other files
bv1to1.conf

161

This conﬁguration ﬁle is a text ﬁle that describes the conﬁguration for the One-To-One environment.
The ﬁle has three distinct sections:

l Definitions speciﬁes local variables for use in subsequent substitutions. Variable values can be

speciﬁed in-line, or evaluated at runtime. This section is described next.

l Export environment variables deﬁnes environment variables needed by One-To-One clients and
services. For information about this section, see “Export environment variables” on page 163.

l Site configuration deﬁnes the physical and logical organization of the site, including the services

in the site, and the parameters of each. For information about this section, see “Site
conﬁguration” on page 166.

Each section begins with a keyword that identiﬁes the section. Following is a sample skeleton of the
arrangement of the sections in the ﬁle:

define

# Variables for substitution

export

# Variables for use by One-To-One and its clients

site siteName {

# Global configurations
process processName {

# Process parameters

}

service serviceName {

# Service parameters

}

group groupName {

# Services and configurations to group together
process processName {

# Process parameters

}

service serviceName {

# Service parameters

}

service serviceName {

# Service parameters

}

}

}

You can include comments in the ﬁle by beginning the comment with an octothorpe (#). All text
from the octothorpe to the end of the line is a comment and is ignored by bvconf.

Installation and Administration Guide

BroadVision, Inc.

162

Chapter 9 Utilities and other files
bv1to1.conf

Deﬁnitions

The deﬁnitions section begins with the define keyword, and speciﬁes local variable deﬁnitions for
use in subsequent substitutions in the conﬁguration ﬁle.

You can deﬁne variable values by hard-coding them in the conﬁguration ﬁle, or by retrieving them
at runtime with one of these three functions:

l $prompt( promptString ) prompts the user for the value, and displays the text as the user

types it in. This function can only be used in the define section.

l $noecho( promptString ) prompts the user for the value, suppresses the text display as

the user types it in, and encrypts the value before substituting it when requested. This function
can only be used in the define section.

l $getenv( variableName ) retrieves the value from a system environment variable. This

function can appear in other sections.

To substitute a variable’s value, use the $arg() function. For example:

# Prompt for the database password
bv_db_passwd=$noecho("Enter DB password: ")
password=$arg(bv_db_passwd)

# Encrypt the password
# Assign it

Database and
password

By default, bv1to1.conf retrieves the database server name, database name, and database user
name from the system environment. It also prompts the user for the database password. You can
change the ﬁle to deﬁne the names instead of retrieving them by removing the comments from the
three deﬁnition lines, and commenting out the three lines that retrieve the variables.

define

# Database parameters.
# Values you provide
bv_dbserver="my_server"
bv_database="my_database"
bv_dbuser="my_user"

#
#
#

# Database server name
# Database name
# Database user name

# Values to get from environment variables
bv_dbserver=$getenv(BV_DB_SERVER)
bv_database=$getenv(BV_DB_DATABASE)
bv_dbuser=$getenv(BV_DB_USER)

# Database server name
# Database name
# Database user name

# Prompt for DB password
bv_db_passwd=$noecho("Enter DB password: ")

# To be encrypted

For more information about the database variables, see “Database variables” on page 33.

BroadVision, Inc.

Installation and Administration Guide

Export environment variables

Chapter 9 Utilities and other files
bv1to1.conf

163

The export environment variables section begins with the export keyword, and deﬁnes
environment variables used by One-To-One clients and services. When you run bvconf execute,
it creates script ﬁles that contain commands that set the environment variables. Run one of the
scripts at least once in a session before any of the One-To-One servers, utilities, or scripts. See “Shell
start-up scripts” on page 39 for details about the script ﬁlenames and location.

Some of the variables deﬁned in this section are used as arguments later in bv1to1.conf. To
substitute a variable’s value for an argument, use $arg. For example, the external database server
name defaults to the One-To-One database server by retrieving the $BV_DBSERVER variable:

ext_dbserver=$arg(bv_dbserver)

Some environment variable values might be reserved characters in a particular shell. If you assign a
character that is reserved by your shell, “escape” the character by enclosing the value in single
quotes. For example, to assign a US dollar sign ($) to the DBMONEY variable:

DBMONEY=’$.’

The bv1to1.conf ﬁle arranges the export section into groups of like deﬁnitions. This tables lists
all of the variables alphabetically, and describes where to get information about using them.

Export variable

Description

AVPAUDIT

AVPIN

AVPOUT

AVPTEMP

BV1TO1

AVP taxing parameter. See “AVP tax program” on page 126.

AVP taxing parameter. See “AVP tax program” on page 126.

AVP taxing parameter. See “AVP tax program” on page 126.

AVP taxing parameter. See “AVP tax program” on page 126.

Basic One-To-One parameter. See “One-To-One variables” on
page 32.

BV1TO1_ROOT_HOST

Name of root host machine. Acquired by bvconf utility.

BV1TO1_VAR

BV1TO1_INSTANCE

Basic One-To-One parameter. See “One-To-One variables” on
page 32.

(Windows NT only) Server instance name. See “Running multiple
One-To-One servers on one host” on page 92.

BV_DB_DATABASE

Basic One-To-One parameter. See “Database variables” on page 33.

BV_DB_SERVER

BV_DB_USER

BV_DB_VENDOR

Basic One-To-One parameter. See “Database variables” on page 33.

Basic One-To-One parameter. See “Database variables” on page 33.

Database vendor identity. See “Database variables” on page 33.

On Windows NT, this is set in registry during installation by Setup.exe.

BV_LC_LIST

BV_LC_MONEY

See “Conﬁguring locales” on page 62

(UNIX only) See “Conﬁguring locales” on page 62

BV_LD_LIBRARY_PATH

One-To-One library search path. See “Search paths” on page 165.

BV_ORB_BIDIRECTIONAL_IIOP Orbix parameter, do not change.

Installation and Administration Guide

BroadVision, Inc.

164

Chapter 9 Utilities and other files
bv1to1.conf

Export variable

Description

BV_ORB_CALL_TIMEOUT

Orbix call connection timeout parameter. Use as a parameter in a
daemon or server deﬁnition to control how long to wait before a call
times out. For example, to wait 15 minutes (900 seconds):

daemon sched_poll_d {

parameter BV_ORB_CALL_TIMEOUT="900"

}

BV_ORB_CONNECT_TIMEOUT Orbix parameter, do not change.

BV_ORB_DIAGNOSTICS

Orbix parameter, do not change.

BV_PATH

BV_RSH_PATH

BV_Y2K_CUTOFF

One-To-One executables search path. See “Search paths” on
page 165.

Shell tool to use for remote calls. See “Remote shell” on page 165.

Year 2000 cut-off date. “Setting the Year 2000 cut-off date” on
page 61.

DBCENTURY (UNIX only)

Informix parameter. See “Informix variables” on page 36.

DBLANG (UNIX only)

Informix parameter. See “Informix variables” on page 36.

DBMONEY (UNIX only)

Informix parameter. See “Informix variables” on page 36.

DSQUERY (UNIX only)

Sybase query server.

INFORMIXDIR (UNIX only)

Informix parameter. See “Informix variables” on page 36.

INFORMIXSERVER (UNIX only)

Informix parameter. See “Informix variables” on page 36.

INTL_CURRENCY (UNIX only) Obsolete. See “Conﬁguring locales” on page 62

intl_currency

Command Center currency. See “Conﬁguring locales” on page 62

INTL_PRECISION (UNIX only)

Obsolete. See “Conﬁguring locales” on page 62

IT_CONNECT_ATTEMPTS

Orbix parameter, do not change.

IT_DAEMON_PORT

Port that the Orbix daemons use to communicate to each other. See
“One-To-One variables” on page 32.

IT_DAEMON_SERVER_BASE

First port that the Orbix daemon may assign to an Orbix server.

IT_DAEMON_SERVER_RANGE Starting at IT_DAEMON_SERVER_BASE, these are the range of

ports that will be assigned to Orbix servers.

IT_MAX_MESSAGE_SIZE

Orbix parameter, do not change.

LANG (UNIX only)

Default system locale. See “Conﬁguring locales” on page 62.

LC_NUMERIC (UNIX only)

Formats numbers. See “Conﬁguring locales” on page 62

LD_LIBRARY_PATH
(Solaris only)

One-To-One/Solaris shared library search path. See “Search paths”
on page 165.

NLS_LANG

NLSPATH

ORA_NLS

ORACLE_HOME

ORACLE_SID

ORACLE_TERM

ORBIX_ACL

Oracle parameter. See “Oracle variables” on page 33.

Tells One-To-One where to ﬁnd its localized messages. Do not
change this deﬁnition.

Oracle NLS location.

Oracle parameter. See “Oracle variables” on page 33.

Same as $BV_DB_SERVER. See “Database variables” on page 33
for details about $BV_DB_SERVER.

Oracle parameter.

Orbix parameter, do not change.

SHLIB_PATH (HP-UX only)

One-To-One/HP-UX shared library search path. See “Search paths”
on page 165.

BroadVision, Inc.

Installation and Administration Guide

Chapter 9 Utilities and other files
bv1to1.conf

165

Export variable

Description

SYB_CHARSET (UNIX only)

Sybase parameter. See “Sybase variables” on page 35.

SYBASE (UNIX only)

Sybase parameter. See “Sybase variables” on page 35.

TNS_ADMIN (UNIX only)

Oracle parameter. See “Oracle variables” on page 33.

Search paths

One-To-One searches for ﬁles in directories speciﬁed by the system search path environment
settings. The deﬁnitions in the bv1to1.conf conﬁguration ﬁle are speciﬁc to One-To-One. When you
run One-To-One, it appends these settings to the system environment settings.

l The BV_PATH settings tell One-To-One where to look for executables. These locations get

appended to your system $PATH variable.

l The BV_LD_LIBRARY_PATH setting contains that directories that the system searches when

looking for shared libraries on UNIX. These values get appended to the variable appropriate for
your platform.

System variable

Looks for

Solaris

HP-UX

$LD_LIBRARY_PATH

.so shared library ﬁles

$SHLIB_PATH

.sl shared library ﬁles

Extend BV_LD_LIBRARY_PATH to include the directories that contain your component and
Dynamic Object shared library ﬁles, if any. This applies to any libraries your components,
application, or Dynamic Objects need. Objects that don’t ship with One-To-One are likely to
have dependencies on other libraries. If the paths to these libraries aren’t present in the
environment deﬁned in bv1to1.conf, the Interaction Manager fails to load them because the
linker isn’t able to ﬁnd the dependents.

The One-To-One schema generator (sch_gen) requires the Rogue Wave libraries be included
in the library variable. To set your variables correctly, source one of the Shell start-up scripts
[See “Shell start-up scripts” on page 39].

Remote shell

On UNIX, bvconf uses a remote shell to execute commands on remote hosts. However, for security
reasons, some sites do not allow applications to run remote shells. If you have another utility that
performs the remote shell functionality, you can tell bvconf to use that utility with the
BV_RSH_PATH parameter. For example, to use ssh instead of the default:

# Override path to remote shell command
BV_RSH_PATH="/opt/local/bin/ssh"

You can override this setting with the bvconf precheck process.

Installation and Administration Guide

BroadVision, Inc.

166

Chapter 9 Utilities and other files
bv1to1.conf

Site conﬁguration

site

The site section deﬁnes the physical and logical organization of the site. Logically, a site contains
services. Physically, a site runs as a set of processes on one or more host machines. Some processes
are site-level (such as the Visitor Management system database server), while others are service-
level (such as the Order Management server). Additionally, you can optionally group service-level
processes into clusters for load balancing using the group construct. The general syntax of the unit
in this section is:

site | group | service | daemon | process { parameter name = value... ;

The site, process and service deﬁnitions are mandatory; group is optional. The scoping of
parameters within an unit is hierarchical, as in the C language. Parameter names are case-sensitive.

Immediately following the site declaration is the name of the site. By default, the site name is bv.
To specify your site’s name, change the declaration; the name must contain ASCII characters only.

site bv {

Use the bvconf execute -S site parameter to work on a specific site. See “Site parameter” on
page 97 for mote information.

Immediately following the site declaration is the global parameter deﬁnitions. These deﬁnitions
tell One-To-One where to ﬁnd databases, and where to locate services in the namespace. You should
not have to change these settings. However, you might have to override some of them later in the
ﬁle, such as within a service or group declaration.

#Global parameters
parameter
...

The bv1to1.conf ﬁle arranges the site section into groups of like deﬁnitions. This tables lists all
of the variables alphabetically, and describes where to get information about using them.

Site parameter

agencydb_path

avp_open_retries

Description

Incentive agency server’s name space location. Do not change.

Taxing, see “Conﬁguring the Taxing system” on page 126.

bv_check_want_message_attr

Notiﬁcations, see “Conﬁguring visitor notiﬁcations” on page 69.

bv_email_delivery_addr_attr

Notiﬁcations, see “Conﬁguring visitor notiﬁcations” on page 69.

bv_email_delivery_server_count Notiﬁcations, see “Conﬁguring visitor notiﬁcations” on page 69.

bv_email_host

bv_js_library_dir

Notiﬁcations, see “Conﬁguring visitor notiﬁcations” on page 69.

Directory of JavaScript component shared libraries.

bv_schedule_dynamic_msgcount Notiﬁcations, see “Conﬁguring visitor notiﬁcations” on page 69.

bv_schedule_keep_messages

Notiﬁcations, see “Conﬁguring visitor notiﬁcations” on page 69.

bv_schedule_msg_dir

Notiﬁcations, see “Conﬁguring visitor notiﬁcations” on page 69.

bv_schedule_parallel_count

Notiﬁcations, see “Conﬁguring visitor notiﬁcations” on page 69.

bv_schedule_script_root

Notiﬁcations, see “Conﬁguring visitor notiﬁcations” on page 69.

BroadVision, Inc.

Installation and Administration Guide

Chapter 9 Utilities and other files
bv1to1.conf

167

Site parameter

Description

bv_schedule_startup_root

Notiﬁcations, see “Conﬁguring visitor notiﬁcations” on page 69.

bv_schedule_static_msgcount

Notiﬁcations, see “Conﬁguring visitor notiﬁcations” on page 69.

bv_site_id

cat_cache_size

cmsdb_path

Site ID, see “Changing the site ID” on page 91.

Content cache, see “Conﬁguring caching” on page 58.

Visitor database accessor’s name space location. Do not change.

cnt_type_cache_size

Content cache, see “Conﬁguring caching” on page 58.

cntdb_path

database

dblib

dbserver

dbuser

default_city

Content accessor’s name space location. Do not change.

One-To-One database name.

DBMS library.

Database server used by One-To-One.

Database access user (account) for One-To-One.

Shipping, see “Computing Shipping Costs” on page 127.

default_cnt_cache_size

Content cache, see “Conﬁguring caching” on page 58.

default_country

default_locality

Shipping, see “Computing Shipping Costs” on page 127.

Shipping, see “Computing Shipping Costs” on page 127.

default_pmt_methods

Payment handling, see “Conﬁguring payment handling” on page 130.

default_postal_code

Shipping, see “Computing Shipping Costs” on page 127.

default_service

discdb_path

external_content_write

external_proﬁle_write

Default service for the site, see “Naming your site and default service.

Discussion group server’s name space location. Do not change.

External content database permission, see “Conﬁguring database
accessors” on page 66.

External proﬁle database permission, see “Conﬁguring database
accessors” on page 66.

gdb_query_cache_size

Content cache, see “Conﬁguring caching” on page 58.

gdb_query_cache_timeout

Content cache, see “Conﬁguring caching” on page 58.

gdb_query_limit

ignore_cache_limit

incndb_path

Content cache, see “Conﬁguring caching” on page 58.

Content cache, see “Conﬁguring caching” on page 58.

Incentive server’s name space location. Do not change.

initial_user_proﬁle_attrs

Proﬁle cache, see “Conﬁguring caching” on page 58.

match_cat_preload

max_idle_time

null_category

Content cache, see “Conﬁguring caching” on page 58.

Count of minutes to wait for an idle database server before
disconnecting and the reconnecting.

Command Center label, see “Changing the “Unclassiﬁed” content
label” on page 54.

observation_ﬂag

Observations, see “Conﬁguring observation logging” on page 80.

observation_ﬂush_time

Observations, see “Conﬁguring observation logging” on page 80.

of_path

ofbe_path

ofdb_path

param_ﬁle

password

Order fulﬁllment server’s name space location. Do not change.

Order back-end server’s name space location. Do not change.

Order management server’s name space location. Do not change.

Payment handling, see “Conﬁguring payment handling” on page 130.

One-To-One database password (encrypted).

pmt_addr_from_proﬁle

Payment handling, see “Conﬁguring payment handling” on page 130.

privacy_ﬂag

Privacy attributes ﬂag. See the Database Administrator’s Guide for
details.

Installation and Administration Guide

BroadVision, Inc.

168

Chapter 9 Utilities and other files
bv1to1.conf

Site parameter

profdb_path

Description

Visitor proﬁle server’s name space location. Do not change.

query_cache_size

Content cache, see “Conﬁguring caching” on page 58.

query_cache_timeout

Content cache, see “Conﬁguring caching” on page 58.

query_limit

rule_cache_size

ruledb_path

Content cache, see “Conﬁguring caching” on page 58.

Content cache, see “Conﬁguring caching” on page 58.

Rule server’s name space location. Do not change.

save_member_limit

Content cache, see “Conﬁguring caching” on page 58.

ship_calc_mode

simple_ship_rate

simple_tax_rate

smgr_ﬁrst_port_minimum

smgr_ip_bvsm

srfac_path

stedb_path

tax_calc_mode

taxon_range_lower

taxon_range_upper

taxon_sort_order

Shipping, see “Computing Shipping Costs” on page 127.

Shipping, see “Computing Shipping Costs” on page 127.

Taxing, see “Conﬁguring the Taxing system” on page 126.

Interaction Manager ﬁrst port address. See “Ports and IP addresses”
on page 108.

Interaction Manager IP and port list. See “Ports and IP addresses” on
page 108.

SalesRep server’s name space location. Do not change.

Site server’s name space location. Do not change.

Taxing, see “Conﬁguring the Taxing system” on page 126.

Matching Agent, see “Conﬁguring the Matching Agent” on page 81.

Matching Agent, see “Conﬁguring the Matching Agent” on page 81.

Matching Agent, see “Conﬁguring the Matching Agent” on page 81.

taxon_use_binary_val_for_cnt

Matching Agent, see “Conﬁguring the Matching Agent” on page 81.

log_sig

See the “Log signal” description that follows this table.

allow_multiple_feedback

See the “Visitor Feedback” description that follows this table.

record_content_feedback

See the “Visitor Feedback” description that follows this table.

Log signal

When the One-To-One servers receive a system signal #1, they re-evaluate their conﬁguration to use
the settings from their appropriate log ﬁle. The log_sig parameter speciﬁes the signal that the
server process looks for. By default, this setting applies to all One-To-One servers in the site.

log_sig="1"

You can assign this setting to individual processes by specifying this setting as a parameter of a
process, like this:

process bvconf_srv { parameter log_sig="2" }

Then, to send the signal to the process, ﬁrst locate its system process ID with the ps command, then
send the signal with the kill command to the process, such as this command that sends signal 2 to
the process whose PID is 23005:

% kill -2 23005

BroadVision, Inc.

Installation and Administration Guide

One-To-One
Command Center
parameters

The One-To-One Command Center displays currency with the currency symbol deﬁned for the
server by the intl_currency parameter.

intl_currency="USD"

Chapter 9 Utilities and other files
bv1to1.conf

169

The One-To-One Command Center requires a Windows character encoding that typically doesn’t
match the encoding that the servers provide. The encoding_type speciﬁcation deﬁne that
character encoding that the One-To-One Command Center is using. The servers then map the
character to match that character set. The possible values are: EUC, and MBCS

encoding_type="EUC"

One-To-One Command Center users can view and update some ﬁles used by the Interaction
Manager and Notiﬁcation servers. When a One-To-One Command Center user attempts to look at
one of these ﬁles, the One-To-One Command Center defaults to look in a directory identiﬁed by one
of the following settings. If the setting is empty, the One-To-One Command Center presents a
directory browser for the user to pick the location.

bv_dcc_document_root=""
bv_dcc_script_root=""
bv_dcc_template_root=""
bv_dcc_schedule_root=""

# Where the HTTPD looks for files.
# JavaScripts.
# Page templates.
# Notification scripts.

Visitor Feedback The Visitor Feedback system collects visitor ratings for site content. By default, this feature is on. To

turn it off, set the record_content_feedback setting to 0.

record_content_feedback="1"

# 1 is on/ 0 is off

When the system is collecting visitor feedback, it allows the visitor to make multiple submissions
(ratings) for the same content item. To restrict visitors to one submission per session, set the
allow_multiple_feedback parameter to 0.

allow_multiple_feedback="0"

# 1 is on/ 0 is off

See the Database Administrator’s Guide for details about visitor feedback attributes.

process

Following the global parameters are the global (site-level) processes. By default, the conﬁguration
runs the process on the root host machine. The process and daemon deﬁnitions must follow all
parameter deﬁnitions in the ﬁle. Processes are started in the order listed in the ﬁle, and they are shut
down in the reverse order. As such, it is important that bvconf_srv and adm_srv be listed ﬁrst.
Also, any processes that depend on other processes should follow the dependency.

Installation and Administration Guide

BroadVision, Inc.

170

Chapter 9 Utilities and other files
bv1to1.conf

Processes inherit settings from the parameter deﬁnitions. Some of these can be overridden, while
other parameters are unique to processes.

Parameter

Processes Daemons Description

host

Yes

Yes

iiop_port

port_assign

Yes

Yes

No

No

shutdown

Yes

Yes

diagnostics

Yes

No

Name of machine on which a server or daemon will run. Do not
change this for bvconf_srv. At runtime when there is a lot of
visitor activity, some servers can get overloaded. To help reduce
the load on a server, you can run multiple instances of some
servers on the same host, or load balance them by distributing the
instances on different hosts.

IIOP well-known port for a server.

Mechanism for assigning well-known IIOP port. Default is
"iiop_wrapper". If "orbixd", take the dynamic port assigned by
orbixd.

Command to run to shutdown the server or daemon. bvconf
appends the unique_pid and the Unix process id of the
server/daemon to this command. It is ignored during forced
shutdown (i.e. bvconf shutdown -f). If this is undeﬁned, bvconf
uses kill.

Orbix diagnostic level. This parameter speciﬁes how much
diagnostic information the process writes to the log ﬁle. It takes the
following values:

0 — errors only (default)
1 — debugging information
2 — verbose Orbix debugging messages.

Here is an example that distributes some of the processes:

# Global processes. You can add more instances, if allowed.
process bvconf_srv {}
process adm_srv {}
process cmsdb {

parameter host = "mars"
diagnostics = "1" }

process cmsdb {

parameter host = "venus" }

process cntdb {}
process cntdb {}
process hostmgr {

parameter host="jupiter" }

# can have only 1 instance
# can have only 1 instance
# 1st instance
# run it on mars
# include some debugging messages
# 2nd instance (can have more)
# run it on venus
# 1st instance
# 2nd instance (can have more)
# can have more instances
# run it on jupiter

BroadVision, Inc.

Installation and Administration Guide

Chapter 9 Utilities and other files
bv1to1.conf

171

Here is a list of all the One-To-One process and daemon servers. For details about conﬁguring these,
see the indicated references. The Multiple column indicates those servers that can have multiple
instances.

Server

adm_srv

alert_srv

Multiple Description

No One-To-One user administration server. There must be one.

No

Alert server handles direct IDL function calls to the Alert system. Other than
that, the rest of the functionality is handled by sched_srv. If your site does
not call the Alert system directly, you can comment out the alert_srv
deﬁnition. [“Conﬁguring visitor notiﬁcations” on page69]

bvconf_srv

No One-To-One conﬁguration management server. There must be one.

cmsdb

Yes Visitor management database server. [“Conﬁguring database accessors” on

page66]

cntdb

Yes Content database server. [“Conﬁguring database accessors” on page66]

deliv_smtp_d

Yes Notiﬁcation delivery server for e-mail type messages. Each instance of this
server must have its own ID, numbered sequentially starting with "1".
[“Conﬁguring visitor notiﬁcations” on page69]

deliv_comp_d

No

Notiﬁcation delivery completion processor. [“Conﬁguring visitor notiﬁcations”
on page69]

extdbacc

Yes External database accessor. You need at least one for each external data

source. [“Conﬁguring database accessors” on page66]

genericdb

Yes Generic database accessor handles content query requests from

applications, when speciﬁcally called from the application. This is also used
by the One-To-One Command Center.

hostmgr

Yes Deﬁnes a host manager process for each machine that participates in

One-To-One, but doesn’t run any One-To-One servers. For example, you
need a hostmgr on a machine that runs only Interaction Manager servers.
You don’t need a separate hostmgr on machines that already has one of the
servers in this list. This process also creates a new $BV1TO1/log
subdirectory for each additional the host, if the directory doesn’t already exist.
This example deﬁnes a host manager process to run on a machine named
“jupiter”:

process hostmgr { parameter host="jupiter" }

ofbe_srv

ofdb

No Order fulﬁllment back-end server.

Yes Order fulﬁllment database server. [“Conﬁguring database accessors” on

om_srv

No Order management server.

page66]

pmtassign_d

No

pmthdlr_d

Yes

The payment archiving daemon routes payment records to the archives by
periodically checking the invoices table looking for records with completed
payment transactions, and then moving those records into an archive table.
[“Conﬁguring payment handling” on page130]

For each payment processing method, you need one or more authorization
daemons to periodically acquire the authorization when a request is made.
There must be at least one pmthdlr_d process for each payment method
listed in the default_pmt_methods parameter. [“Conﬁguring payment
handling” on page130]

Installation and Administration Guide

BroadVision, Inc.

172

Chapter 9 Utilities and other files
bv1to1.conf

service

Server

Multiple Description

pmtsettle_d

Yes Payment settlement daemon periodically checks the database for orders of

the associated payment processing method that need to be settled, and then
authorizes the transactions. [“Conﬁguring payment handling” on page130]

sched_poll_d

No

Notiﬁcation schedule poller scans the database tables to determine when a
notiﬁcation must be run. [“Conﬁguring visitor notiﬁcations” on page69]

sched_srv

Yes Notiﬁcation schedule server runs the scripts that generate the visitor
notiﬁcation messages. [“Conﬁguring visitor notiﬁcations” on page69]

By default, the conﬁguration ﬁle creates two services named Mall and MyBank. To specify your
service’s name, change the declarations; the name must contain ASCII characters only. Additionally,
to populate the service descriptor database table (BV_STORE) with the service’s attributes, declare
the attributes as parameters to the service; the parameter names must match the column names
deﬁned the stores database schema. You can omit any or all parameters at your discretion. The
following example deﬁnes the parameters for the MyBank service:

service MyBank {
parameter
email_address = "mybank-mgr@broadvision.com"
postal_address = "12345 Main St, San Jose, CA"
www_url = "mybank.broadvision.com"
phone_number = "800-555-1234"
fax_number = "800-555-1235"
pmttype_id = "0, 1, 2"
other1 = "Customer Service: P.O. Box 5, Los Altos, CA"
# Override the global payment processing methods if necessary.

}

group

All stores use all processes deﬁned at the global (site) level, unless you specify otherwise. The
group unit allows you to identify which processes to use with which services. Use groups to
provide load balancing of processes between services. For example, the One-To-One Command
Center uses a content database accessor (cntdb), to keep it from using the same one that you Web
application is using, assign the cntdb process to the “CommandCenter” group (this is a reserved
group name).

# The One-To-One Command Center tries to use servers in its own group
#  first.  Currently only cntdb may be placed in this group.
#
group CommandCenter {

process cntdb {}     # can have more instances

}

BroadVision, Inc.

Installation and Administration Guide

Chapter 9 Utilities and other files
bv1to1.conf

173

Or, two small services might share the same Order Management process, while another larger
service would have its own. For example, to create a group of Order Management process to a
group called group1, and to assign two services to that group:

group group1 {

parameter

param_file=$env(BV1TO1)+"/bin/omnihost.cfg"

process ofbe_srv {}
process om_srv {}
process ofdb {}

# can have only 1 instance
# can have only 1 instance
# can have more instances

service BestBuyClothing {

parameter
email_address = "mgr@bestbuyclothing.com"
postal_address = "12345 Main St, San Jose, CA"
www_url = "www.bestbuyclothing.com"
phone_number = "800-555-1234"
fax_number = "800-555-1235"
pmttype_id = "0, 1, 2"
other1 = "Customer Service: P.O. Box 5, Los Altos, CA"

}

service SuperDuperBooks {

parameter
email_address = "mgr@superduperbooks.com"
www_url = "www.superduperbooks.com"
phone_number = "800-555-5678"
pmttype_id = "0, 1, 2"

}

}

}

Installation and Administration Guide

BroadVision, Inc.

174

Chapter 9 Utilities and other files
bvconf

bvconf

Use bvconf to start, restart, conﬁgure, and shutdown the One-To-One services. This one script is
your interface to conﬁguring and controlling the services, and you can run most of its processes
while the services are up and running.

Be sure to back up bv1to1.conf after any configuration changes. See “Backing up your site”
on page 141 for details.

Whenever you make a change to your conﬁguration ﬁle, run bvconf syntax_check to test
the validity of the changes before you execute the changes. For more information, see
“syntax_check” on page 183.

You specify which bvconf process as the ﬁrst argument to the script. Each process can have its own
argument list.

Never run bvconf as a root user.

Syntax

bvconf [ execute | dump | shutdown | restart | help | monitor |

ns | ping | precheck | ps | smap | syntax_check ]

Location

$BV1TO1/bin/

Usage

Each process and its syntax is described in detail in the following sections.

l dump is described next

l execute is on page 175

l help is on page 177

l monitor is on page 177

l ns is on page 177

l ping is on page 178

l precheck is on page 179

l ps is on page 179

l restart is on page 181

l shutdown is on page 181

l smap is on page 182

l syntax_check is on page 183

BroadVision, Inc.

Installation and Administration Guide

Chapter 9 Utilities and other files
bvconf

175

dump

Reads the current conﬁguration settings from the binary ﬁle and dumps them into a text ﬁle
formatted similar to the conﬁguration source ﬁle.

Syntax

bvconf dump

You specify conﬁguration settings in the bv1to1.conf text conﬁguration ﬁle. When you run
bvconf, it compiles the information in that ﬁle into a binary ﬁle that the system reads for its
conﬁguration requests. This dump process reverses the process by reading the binary ﬁle and
generating an ASCII text ﬁle that contains the conﬁguration settings; the new ﬁle does not contain
any comments from the original source ﬁle. You can use the new ﬁle as input to bvconf to compile
a new binary ﬁle.

Usage

execute

Conﬁgures and starts the One-To-One services.

If you have already configured the system, you can skip the configuration process and just start
the services with the restart process, as described on page 181.

Syntax

bvconf execute [ -p ] [ -s sourceFile ] [ -n ] [ -d ] [-S siteName ]

[ -i instance_name ]
[ -a { install_all | install_servicedb | incremental } ]

-a install_all

install_servicedb
incremental

Update the service databases based on the conﬁguration information. By
default, bvconf uses incremental, which updates that databases with
any new conﬁguration information. If no changes are speciﬁed, no
changes occur.

Use install_all when you ﬁrst install the databases. This tells
bvconf to deﬁne the databases based on the information in the
conﬁguration ﬁle. It also removes the $BV1TO1_VAR/messages/
subdirectories, these contain the Notiﬁcation messages.

Use install_servicedb when you want to replace the service
descriptor database with the speciﬁcations in the conﬁguration ﬁle. The
descriptor database includes the information that describes the service,
such as its name, phone number, address, and such. You can update or
change this database by using incremental, but if you want to replace
it all, use install_servicedb instead.

Turns on logging of Orbixd by writing a terse log ﬁle to
$BV1TO1_VAR/logs/hostName/orbixd.log.

Name of the One-To-One instance to start. You need to name each
instance when you run mulltiple instances of the One-To-One servers on
the same machine. See “Running multiple One-To-One servers on one
host” on page 92 for details.

Suppress the execution of dump_taxon, which updates the Matching
Agent cache.

-d

-i instance_name
(Windows NT only)

-n

Installation and Administration Guide

BroadVision, Inc.

176

Chapter 9 Utilities and other files
bvconf

-p

-s sourceFile

Prompt for database access password. bvconf always prompts for the
password the ﬁrst time you run the script. It then stores the password in an
encrypted form, and uses the stored one for subsequent accesses. If you
change the database user password, run bvconf with this argument to
re-prompt for the password and to replace the stored version.

The conﬁguration ﬁle to use. If you omit this option, bvconf ﬁrst attempts
to use $BV1TO1_VAR/etc/bv1to1.conf, if that ﬁle doesn’t exist,
bvconf uses $BV1TO1_VAR/lib/bv1to1.conf.default.
Regardless of where your sourceFile is, bvconf copies it to
$BV1TO1_VAR/etc/bv1to1.conf.

-S siteName

The name of the site, as deﬁned by the site parameter, to start. See “Site
parameter” on page 97 for details.

Usage

All One-To-One services are conﬁgured with bvconf. The conﬁguration process begins with source
speciﬁcation ﬁle: $BV1TO1_VAR/etc/bv1to1.conf. This ﬁle is a text ﬁle that you use to deﬁne
the One-To-One environment, including environment variables, site and service conﬁguration, and
server load balancing arrangements. If you do not have this ﬁle in the indicated directory, and if you
omit the -s option, bvconf reads the default ﬁle, $BV1TO1_VAR/lib/bv1to1.conf.default,
and uses its deﬁnitions to create the correct ﬁle in the etc directory.

Never run bvconf as a root user.

When you change or create a conﬁguration with bvconf, it compiles bv1to1.conf into a version
named bv1to1.conf.o. This binary ﬁle is optimized for machine processing, and contains the
transient information deﬁned in the deﬁne section of the conﬁguration ﬁle.

If you reconﬁgure the system by changing bv1to1.conf and then rerunning bvconf execute,
the process creates a ﬁle, bv1to1.conf.delta, which contains the differences between the
previous conﬁguration and the new one. This ﬁle is used for incremental updates.

Here are some additional notes about using this process:

l Run the execute process while the system is stopped. To stop the services, use bvconf

shutdown, which is described on page 181.

l You must run the execute process whenever you make a change to the conﬁguration,

including One-To-One server and Interaction Manager conﬁguration changes.

l The execute process checks and restores the system management state to a consistent state. If

you have problems with the One-To-One system, try running this process.

l When you back up your system, be sure to save a copy of bv1to1.conf as source or printout

to assist in recreating your environment.

l Whenever you make a change to your conﬁguration ﬁle, run bvconf syntax_check to test

the validity of the changes before you execute the changes. For more information, see
“syntax_check” on page 183.

l Running the execute process on a “healthy” system does not alter the existing system’s

conﬁguration.

l If the process terminates with an error about the site ID being different, correct the problem per

the instructions in “Changing the site ID” on page 91.

The One-To-One services require some environment variables be deﬁned at runtime. To assist you in
correctly deﬁning the environment variables, bvconf generates text ﬁles that can be sourced
directly by csh, sh, or ksh. The two ﬁles, bv1to1.conf.csh and bv1to1.conf.sh, both reside
in $BV1TO1_VAR/etc/.

BroadVision, Inc.

Installation and Administration Guide

Chapter 9 Utilities and other files
bvconf

177

help

The help process displays syntax for all of the bvconf processes.

Syntax

bvconf help

monitor

ns

Reports on the usage statistics of One-To-One servers and processes, and has three modes of
operation: report, interactive, and explore. The latter two modes are used mainly for debugging and
testing CORBA servers. The former is discussed in detail in “Monitoring server statistics” on
page 145.

The ns process displays the namespace for the current One-To-One environment, and optionally
can update objects in a name space.

Syntax

bvconf ns [ -H hostName { -g nameSpace | -p nameSpace | -P } ]

-g nameSpace Get objects from the named host’s namespace and add or update them to the current

host. See “Updating name space objects across sites” on page 98 for details.

-H hostName

Name of host to query or update.

-p nameSpace Place objects from the current host into the named host’s namespace.

-P

Place objects from the current host into all namespaces.

Installation and Administration Guide

BroadVision, Inc.

178

Chapter 9 Utilities and other files
bvconf

Usage

Developers writing C++ applications that connect to the One-To-One APIs need to know the
conﬁguration of the servers within the One-To-One environment. The ns process reports the
conﬁguration in a text format, similar to this:

"agencydb1"
"agencydb2"

"ruledb2"
"ruledb1"

"cntdb1"
"cntdb2"

"CntDB"
|
|
"AgencyDB"
|
|
"DiscDB1"
"RuleDB"
|
|
"IncentiveDB"
|

"CntMgmt"
|
|
|
|
|
|
|
|
|
|
|
|
"Store1"
|
|
|
"CMS"
|
|
|
|
|
"AdminManager"

"CMSDB"
|
|
"ProfileDB"
|

"OrderMgmt"
|
|

"cmsdb1"
"cmsdb2"

"incndb1"

"profdb1"

"PmtHdlr"
|

"pmthdlr1"

The -g and -p options respectively “get” or “push” from or to the remote host. Objects in the source
context not already in the target are added to the target. For example, to get the Interaction Manager
objects (bvsmgr) from a machine name earth onto the current machine:

$ bvconf ns -H earth -g bvsmgr

To push from the current machine to earth:

$ bvconf ns -H earth -p bvsmgr

ping

Syntax

Usage

The ping process veriﬁes that One-To-One servers are up and running, and optionally, can launch a
server not already running. This command passes all options directly to the bvping utility. See that
command for a description of the options.

bvconf ping options command

See the description of bvping on page 188 for details.

BroadVision, Inc.

Installation and Administration Guide

Chapter 9 Utilities and other files
bvconf

179

The precheck process with its -r option identiﬁes the remote shell to use when running command
on remote hosts. This setting overrides the BV_RSH_PATH setting in the bv1to1.conf
conﬁguration ﬁle. For more information, see “Remote shell” on page 165.

bvconf precheck [[ -r remoteShell ] host ]

When specifying the remote shell, include the full path to the ﬁle. For example, to use ssh instead
the default:

bvconf precheck -r /opt/local/bin/ssh smidgen

precheck

Syntax

Usage

ps

The ps process displays information about the One-To-One servers.

Syntax

bvconf ps [ -l [ 0 | 1 | 2 ]] [ -c ] [ -d ] [ -D ] [-g group ]

[ -h [ host ]] [ -H ] [ -Z | -z ]

-c

-d

-D

-g group

-l [ 0 | 1 | 2 ]

Lists the static conﬁguration information about the process.

Lists daemons only.

Includes daemon processes in addition to ORB servers.

Reports a speciﬁc group; default is all groups in site.

Speciﬁes the level of information to display about the server. The default,
0, reports the unique, One-To-One process ID, the name of the server’s
executable, the host that the server is running on, its port, and process ID.

Level 1 reports the level 0 information, and additionally reports UNIX ps
information, including the CPU load, start time, and installation of the
server.

Level 2 reports the level 1 information, and additionally reports the length
of time that the server has been running, and the complete path of the
command that started the server.

-h [ host ]

Lists remote machines only, or for the speciﬁed machine only.

-H

-Z

-z

Lists the processes on all host machines in the One-To-One environment.
By default, the ps process lists the servers on the current host only.

Lists all servers that have been conﬁgured, including those that are not
currently running

Lists the servers that have been conﬁgured, but which aren’t currently
running.

Installation and Administration Guide

BroadVision, Inc.

180

Chapter 9 Utilities and other files
bvconf

Usage

By default, the ps process only shows information about the servers running in the current host,
similar to this:

% bvconf ps
UNIQPID
p_2700_2
p_2700_4
p_2700_3
p_2700_5

TYPE
EXEC
objsrv bvconf_srv
objsrv cmsdb
objsrv cmsdb
objsrv cntdb

HOST
mars
mars
mars
mars

PORT
1302
1308
1307
1309

PID
24118
24338
24337
24824

To see information about all conﬁgured servers, including ones that aren’t running, use -Z:

% bvconf ps -Z
UNIQPID
p_2700_2
p_2700_4
p_2700_3
p_2700_5
p_2700_1
p_2700_6

EXEC
TYPE
objsrv bvconf_srv
objsrv cmsdb
objsrv cmsdb
objsrv cntdb
objsrv adm_srv
objsrv cntdb

HOST
mars
mars
mars
mars
mars
mars

PORT
1302
1308
1307
1309
-
-

PID
24118
24338
24337
24824
-
-

To see which conﬁgured servers are currently not running on all hosts, use -H and -z:

% bvconf ps -H -z
UNIQPID
p_2700_1

TYPE
objsrv adm_srv

EXEC

HOST
mars

PORT
-

PID
-

To see all servers that have been conﬁgured, and include all daemon processes, use -D and -Z:

objsrv cmsdb
objsrv sched_srv

% bvconf ps -Z
EXEC
TYPE
UNIQPID
daemon pmtassign_d
d_1221_9
p_1221_4
objsrv cntdb
d_1221_12 daemon deliv_comp_d mars
p_1221_3
p_1221_6
d_1221_11 daemon deliv_smtp_d mars
p_1221_8
d_1221_10 daemon sched_poll_d mars
p_1221_1
p_1221_2
p_1221_5
p_1221_7

objsrv bvconf_srv
objsrv adm_srv
objsrv sched_srv
objsrv alert_srv

objsrv genericdb

HOST
mars
adrastea

adrastea
adrastea

adrastea

adrastea
mars
mars
mars

PORT

PID
- 10487
1303 10519
- 10508
1307 13102
1305 13101
- 10501
1309 15645
- 10494
1301 10410
-
-
-

-
-
-

BroadVision, Inc.

Installation and Administration Guide

Chapter 9 Utilities and other files
bvconf

181

restart

The restart process restarts the One-To-One services without running the conﬁguration process
that the execute process performs. Can also restart daemons while the rest of the system remains
running.

Syntax

bvconf restart [ -d ] [ serverName [serverName … ] ]

-d

serverName

Restarts all daemons that have stopped,. You do not have to shutdown the
rest of the system to restart daemons.

A speciﬁc server to restart. To get the names of the conﬁgured servers, use
bvconf ps -Z -D.

Usage

Use this process to restart the One-To-One services without running the conﬁguration process. See
the description of execute on page 175 for information about conﬁguration.

If the process terminates with an error about the site ID being different, correct the problem per the
instructions in “Changing the site ID” on page 91.

To start all servers that are conﬁgured, but not currently running, use the -d option:

bvconf resart -d

To restart multiple servers, specify them in the list of server names:

bvconf restart sched_poll_d pmtsettle_d pmthdlr_d

To start Interaction Manager servers, use imgr_conf -a start.

shutdown

Stops the One-To-One services. This command calls bvkill to perform the work.

Syntax

bvconf shutdown [ -f ] [ serverName [serverName … ] ]

-f

Force a shutdown (destroy), same as kill -9. Use this option when the
building is on ﬁre and you have to get out quick. Otherwise, use this only as a
last resort because it will not gracefully stop servers, which can leave jobs in an
undeﬁned state.

serverName

A speciﬁc server to shutdown. To get the names of the conﬁgured servers, use
bvconf ps -Z -D.

Installation and Administration Guide

BroadVision, Inc.

182

Chapter 9 Utilities and other files
bvconf

Usage

Use this process to safely shut down and stop the One-To-One services. By itself, shutdown stops
all One-To-One server processes and daemons. It stops them in the reverse order that they appear in
the bv1to1.conf conﬁguration ﬁle.

bvconf shutdown sched_poll_d

Wait for bvconf to announce that it is “done” before making changes to the system.

Include the server process name to stop just one, or a family of server processes. For example, to
stop just the Notiﬁcations servers, shutdown the sched_poll_d server and it will stop the other
Notiﬁcation servers when they complete their jobs:

bvconf shutdown sched_poll_d

To stop Interaction Manager servers, use imgr_conf -a stop.

To stop multiple servers, specify them in the list of server names:

bvconf shutdown sched_poll_d pmtsettle_d pmthdlr_d

To restart stopped servers, use bvconf restart.

For information about shutting down a One-To-One site, see “Shutting down your site” on
page 138.

smap

Lists the status and IDs of services within the site.

Syntax

bvconf smap [ all | serviceName ]

all

(default) lists the whole service map.

serviceName

Lists the map for the named service.

Usage

The listing includes the service name, online status, and service ID.

BestBuyClothing
Mall
SuperDuperBooks
SuperVideos

Online
Online
Offline
Offline

101
0
102
103

BroadVision, Inc.

Installation and Administration Guide

syntax_check

Chapter 9 Utilities and other files
bvkill

183

Veriﬁes the syntax of your conﬁguration ﬁle.

bvconf syntax_check

You can run this process without shutting down the system. Use this option to test the validity of
your ﬁle before executing the changes. This way you don’t have to keep your system down for long
when making changes. Test the syntax before you shutdown for a conﬁguration change.

Syntax

Usage

bvkill

Shuts down One-To-One processes and servers.

Syntax

bvkill [-v] [-w period] signal upid osPid

Location

$BV1TO1/bin

Usage

You should not have to call this utility directly. Instead, you should use bvconf shutdown, which
hides the details of calling bvkill.

See also

“shutdown” on page 181.

bvlog

Writes a message to a log ﬁle.

Syntax

bvlog level set { message | msgNum [ parameter ... ] }

level

set

Error level of the message. How much information to generate about a message.
Must be a member of the <level_range> values identiﬁed by .bvlog.conf.

Identiﬁes the message set of the message to log. Must be a member of the
<set_range> values identiﬁed by .bvlog.conf.

message

msgNum

A free-form message string to write.

Message number from a message catalog.

parameter

A string that is the formatting pattern to use for formatting the msgNum message.

Location

$BV1TO1/bin

Usage

The message argument is the message to write to the ﬁle. It can be a simple string, such as:

bvlog 1, 1, "Failed to initialize"

Installation and Administration Guide

BroadVision, Inc.

184

Chapter 9 Utilities and other files
.bvlog.conf

Which makes writes “Failed to initialize” as the message in a record in the log ﬁle.

See also

“Conﬁguring observation logging” on page 80 and “.bvlog.conf” on page 184.

.bvlog.conf

The .bvlog.conf conﬁguration ﬁle speciﬁes which One-To-One logging and error activities to
perform, to what level, and where to write the results. Some of the logging activities include
microtransactions and observations. At start-up, bvconf looks for this ﬁle in $BV1TO1_VAR/etc/,
and then, if not there, in your home directory. If it doesn’t ﬁnd the ﬁle, bvconf copies the default ﬁle
from $BV1TO1/lib/bvlog.conf.default to $BV1TO1_VAR/etc/.bvlog.conf.

Usage

Servers that get their conﬁguration from this ﬁle read the ﬁle when they start running. The easiest
way to cause a server to reload its conﬁguration is to stop and then restart the server. Do this with
bvconf shutdown -d and restart -d.

To cause an internal One-To-One server to reload its conﬁguration ﬁle while the server is running,
send a log_sig signal to the server. The log_sig setting deﬁned in bv1to1.conf [see “Log signal”
on page 168], but is usually 1. Identify the server by its process ID (PID), which you can ﬁnd with
bvconf ps. For example, to cause an alerts server (alert_srv) on UNIX to reload its
conﬁguration, ﬁrst learn the server’s PID (such as 13005), and then use the kill command to send
the signal 1:

% kill -1 13005

You can only reload conﬁgurations for internal One-To-One servers: those listed by bvconf ps -z.
All others must be stopped and restarted.

Syntax

Each line in the text ﬁle is either a comment, which is a logging speciﬁcation or catalog speciﬁcation
with either of the following syntax:

<set_range> <level_range> <log_file> [ <format> ]

<message_set> catalog <message_file>

You can comment an entire line by beginning the line with an octothorpe (#), or you can include an
in-line comment line by beginning the comment with double slashes (//).

The bvconf utility processes the line sequentially. As such, you can set default values for a range of
messages in an early line, and override some of the settings in subsequent lines. For example, the
following turns on critical and general error messages (0:1) for all logging activities (0:39), but
turns non-critical errors off for Dynamic Objects (28):

0:39
28

0:1
1:5

DEFAULT
OFF

// Turn on all critical and general errors.
// Leave on only critical errors.

Location

$BV1TO1_VAR/etc/.bvlog.conf
$BV1TO1/lib/bvlog.conf.default

(default source file)

BroadVision, Inc.

Installation and Administration Guide

<set_range>

The <set_range> argument identiﬁes the messages to log. It can either be an integer that speciﬁes
a single message, or a range that identiﬁes a set of messages. To identify a range, specify two
integers separated by a colon (:) and no white space.

Chapter 9 Utilities and other files
.bvlog.conf

185

ID Message (server name)

2 One-To-One Commerce

3 One-To-One Publishing Center

4 One-To-One Financial

5 Utility functions

6 Observation report

7 One-To-One internal

8 One-To-One Knowledge

ID

Message

17 Content management (cntdb)

18

Interaction manager

19 Microtransaction

20 Database (genericdb & extdbacc)

21 Proﬁling (profdb)

22 Discussion groups (discdb)

23

Incentives (incndb)

9 Order Management (om_srv, ofbe_srv, & ofdb)

24 Matching

10 JavaScripts

11 Visitor management (cmsdb)

25 Shell scripts

26 Alerts (alert_srv)

12 Observation-error and -debugging messages

27 Scheduling (sched_srv)

13 Components

14 Performance measurements

15 Orbix

28 Dynamic Objects

29 Payment handler

30 HTTP daemon

16 Administration management (adm_srv)

31-39 Reserved for applications

<level_range>

The <level_range> argument speciﬁes how much information to generate about a message. It
can either be an integer, or a range. To identify a range, specify two integers separated by a colon (:)
and no white space. What information a message produces varies for each message.

ID

Level

0

1

2

3

4

5

Critical errors only. Use this setting for most messages.

Any error.

Any warning.

General information about the message.

Verbose information.

Debugging information. This setting quickly produces megabytes of information for some
messages. Use this only when trying to identify a problem.

Installation and Administration Guide

BroadVision, Inc.

186

Chapter 9 Utilities and other files
.bvlog.conf

<log_ﬁle>

The <log_file> argument identiﬁes where to send the message information. All destinations are
assumed to be ﬁles in the $BV1TO1_VAR/logs/$HOST directory, where $HOST is the name of the
machine that generated the message. If this directory does not exist, the default directory is
/var/tmp. Specify a different directory by beginning the <log_file> argument with a slash (/).
You can use a symbolic link to redirect log output from NFS to a local disk.

The default log ﬁlename is “bvlog.out%”, you can use this value by specifying “DEFAULT” as the
<log_file> value.

A percent symbol (%) at the end of a ﬁlename speciﬁes to include the current date in the log
ﬁlename. When used, the ﬁlename ends with “.CCYYMMDD”, where CCYYMMDD is the current
date.

19

0:5

mtlog%

RAW

// Send microtransactions to mtlog.CCYYMMDD

To turn messaging off, specify “OFF” for the <log_file>; otherwise, log messages are on. For
example, to turn off all but critical error messages for Dynamic Objects:

28

1:5

OFF

// Turn off all but critical errors.

To send messages to the standard output, specify “STDOUT”. For example, to send shell script
message to standard output:

25

0:5

STDOUT

RAW

// Send shell script message to stdout.

<format>

This optional argument speciﬁes the format of log output. What information a message produces
varies for each message.

Value

RAW

Amount of information

All information.

LONG

Most information; this is the default.

SHORT

Some information.

catalog

The logging system can pass a speciﬁc message from a catalog, which is a ﬁle that contains
predeﬁned messages. Each catalog is identiﬁed by a message set. The catalog keyword identiﬁes
message catalogs to associate with a message set, as identiﬁed by the <set_range> parameter.

For example, if a “travel reservation” application is using message set 38, and that application’s
message catalog ﬁle is $BV1TO1/lib/travel.msg, you associate the two with this statement:

38

catalog travel.msg

For information about how to create a message catalog, and how One-To-One accesses the
messages, see the “Observation system” chapter in the API Reference.

See also

“Conﬁguring observation logging” on page 80 and “bvlog” on page 183.

BroadVision, Inc.

Installation and Administration Guide

bvobs.conf

Chapter 9 Utilities and other files
bvobs.conf

187

This conﬁguration ﬁle deﬁnes the information that gets written to the observation log ﬁle. When the
system logs an observation, it writes to the ﬁle the values of the attributes deﬁned in this ﬁle.

One-To-One has 12 predeﬁned and reserved observation types. In addition to these, you can deﬁne
your own observation types. [See the One-To-One Observations Logging and Reporting guide for
details about custom observation types.]

OBSLOG_ENTER_SESSION

0 Generated when visitor logs into site

OBSLOG_END_SESSION

1 Generated when visitor logs out

OBSLOG_IDENTIFY

2 Generated when a visitor proﬁle is created

OBSLOG_ENTER_STORE

3 Generated when visitor enters service

OBSLOG_SELECT

4 Generated when visitor selects content

OBSLOG_SEE

5 Generate when visitor is shown content

OBSLOG_CHOOSE

6 Generated when visitor adds an item to the shopping cart

OBSLOG_REMOVE

7 Not used

OBSLOG_BUY

8 Generated when visitor makes a purchase

OBSLOG_BUY_MT

9 Generated when a microtransaction occurs

OBSLOG_USER_DEFINED

10 Site deﬁned

OBSLOG_TARGETING_RULE 11 Generated when a matching rule is triggered

OBSLOG_EXIT_STORE

12 Not used.

The rest of the ﬁle maps the information collected for each observation type into the attributes of the
table that will contain the loaded raw-observation data. For example, the ﬁrst entry is:

0,SESSION_ID,USER_ID,TIMESTAMP

This maps the login-event to the structure of the BV_ENTER_SESSION table

Attribute

SESSION_ID

USER_ID

TIME_STAMP

Data Type

numeric

integer

datetime

Semantics

Identiﬁes session.

Identiﬁes the visitor in the BV_USER table.

Timestamp (date and time).

For information about the tables, see the Database Schema Reference.

Installation and Administration Guide

BroadVision, Inc.

188

Chapter 9 Utilities and other files
bvping

bvping

The bvping utility veriﬁes that One-To-One servers are up and running, and optionally, can launch
a server not already running.

Syntax

Verify all servers speciﬁed in bv1to1.conf:

bvping options -a

Veriﬁes Interaction Manager (bvsmgr) servers:

bvping options [-h host | -H] [-A appName ] [-E engineId ]

-p bvsmgr

-h host

-H

-A appName

Checks all Interaction Manager servers on the named host.

Checks all Interaction Manager servers on all hosts.

Checks the named Interaction Manager installation. Use “-” for all
installations. See “Running multiple applications on a single CGI host” on
page 111 for information about named installations.

-E engineId

Checks the speciﬁed Interaction Manager engine.

Verify a server by its executable name:

bvping options [ -g group ] [-i instanceId ] -p process

Options

Where options is one of:

[ -t timeout ] [ -d diagnostic ] [ -q ] [ -f ] [ -l ]

-l

-t timeout

Launches the speciﬁed server, if it is not already running.

Orbix connection time out, in seconds. This is how long Orbix should wait
before reporting that the server is not available.

-d diagnostic

Diagnostic level.

-q

-f

Quiet mode. Skips the header information and writes some messages
directly to the log ﬁles instead of to the console.

Read the conﬁguration information from the
$BV1TO1_VAR/etc/bv1to1.conf.o instead of requesting it from the
bvconf_srv server.

Location

$BV1TO1/bin

BroadVision, Inc.

Installation and Administration Guide

Chapter 9 Utilities and other files
bvsm.ACL

189

bvsm.ACL

This is the system’s access control ﬁle.

Location

UNIX default location:

/etc/opt/BVSNsmgr/bvsm.ACL

Windows NT default location:

$BV1TO1_VAR/BVSNsmgr/bvsm.ACL

Source ﬁles

$BV1TO1/lib/bvsm.ACL.default

Usage

For details about this ﬁle, see “Conﬁguring access control” on page 55.

This file must have at least world-readable, world-searchable, and world-writable access
permission (777 on UNIX).

Installation and Administration Guide

BroadVision, Inc.

190

Chapter 9 Utilities and other files
bvsm.cfg

bvsm.cfg

Location

Usage

This is the Interaction Manager and gateway application conﬁguration ﬁle. It is a text ﬁle that
deﬁnes the settings for the Interaction Manager.

UNIX default ﬁle:

/etc/opt/BVSNsmgr/bvsm.cfg

Windows NT default ﬁle:

$BV1TO1_VAR/BVSNsmgr/bvsm.cfg

The imgr_conf utility creates and maintains this ﬁle. You should use that utility instead of
modifying the ﬁle directly. For more information, see “Conﬁguring the Interaction Manager server”
on page 40.

This file must have at least world-readable, world-searchable, and world-writable access
permission (777 on UNIX).

If you are using a named application, this ﬁle is renamed to match the application name, such as
“appname.cfg”

Multiple host conﬁgurations

When the Interaction Manager servers and One-To-One gateway application are on separate
machines that do not share the same ﬁle system, each host has an exact copy of the same ﬁle which
the programs use to determine how to ﬁnd each other. The Interaction Manager always looks for the
ﬁle in the default location (speciﬁed above). The gateway application looks for the ﬁle as follows:

On a UNIX host, the ﬁle is always located in

/etc/opt/BVSNsmgr/

On a Windows NT host, the ﬁle is in the location speciﬁed by this registry key:

\HKEY_LOCAL_MACHINE\SOFTWARE\BroadVision\

One-To-One Application System\4.1\Interaction Manager\
default\export\BV1TO1_SESSION_CFG

If you are using a named application, the application name, such as “appname”, replaces
“default” in the registry path.

On a Windows NT host, another registry key, BVSNSMGR_LOGS, identifies the directory where
the gateway application writes its log file. This and BV1TO1_SESSION_CFG are the only two
keys required by gateway applications on a stand-alone host machine.

See “Ports and IP addresses” on page 108” for information about how the Interaction Manager
communicates with the gateway application.

BroadVision, Inc.

Installation and Administration Guide

Chapter 9 Utilities and other files
bvsm.req

191

bvsm.req

Location

This is the Interaction Manager page request cache conﬁguration ﬁle. It is a text ﬁle that deﬁnes the
settings for the cache.

UNIX default ﬁle:

/etc/opt/BVSNsmgr/bvsm.req

Windows NT default ﬁle:

$BV1TO1_VAR/BVSNsmgr/bvsm.req

Usage

For details about this ﬁle, see “Conﬁguring the page request cache” on page 113.

This file must have at least world-readable, world-searchable, and world-writable access
permission (777 on UNIX).

bvsm_version

Returns a character string that is the version number of the running Interaction Manager servers.

Syntax

bvsm_version

Location

$BV1TO1/bin

Usage

Run this utility with no command-line arguments.

cache_utl

This utility tells an Interaction Manager to reload a data cache.

Syntax

cache_utl { -r option | -e cacheName } [ options ]

-a applicationName

-c key

Speciﬁes a named Interaction Manager. If you omit this option, cache_utl
uses the “default” installation. See “Named applications” on page 104 for
more information about Interaction Manager names.

Load a speciﬁc content item or category as identiﬁed by the content key or
category path. A content key attribute is always the ﬁrst attribute in the table
schema following the OID attribute. For example, the Editorial key attribute is
ED_NAME. To load a speciﬁc editorial, pass the editorial name as a string to
this option, such as “Presidents message”.

For categories, specify the path of the category as a string, such as
“/Products/Mutual_Funds/Portfolio”.

Installation and Administration Guide

BroadVision, Inc.

192

Chapter 9 Utilities and other files
cache_utl

-e cacheName
[-d cacheArgument ]

Identiﬁes a cache to manipulate, and optionally passes an argument to the
process that manipulates the cache. The valid cache names are:

script_cache — manipulates the cache of scripts. The -d arguments are

• disable — disables caching
• enable — enables caching
• flush — ﬂushes the data from the cache
• dump — writes information about the cache’s contents to the log ﬁle

request_cache — manipulates the page request cache. The -d
arguments are the name of the request cache deﬁned in the rules. See
“Changing the request cache dynamically” on page 121 for details.

Displays the usage message for this utility.

Reloads the access control cache. Same as the imgr_acltool utility’s
refreshcache command.

Reloads the category cache

Reloads the content cache

Reloads the collection cache

Reloads the community cache

Dumps the access control cache

Reloads the query cache.

Reloads the Notiﬁcations (scheduler) cache. When you use this option, you
must also specify -s and -t.

Reloads the Matching Agent cache

Speciﬁes the service to affect, can be ALL_STORE for the entire site, or the
names of the site or service as deﬁned in bv1to1.conf.

The content type to affect. Valid options are: ALL_CONTENT, PRODUCT, AD,
EDITORIAL, INCENTIVE, DISCUSSION, and TEMPLATE.

Verbosity ﬂag. When you include this option, cache_utl generates status
messages; otherwise, it runs silent,

-H/h

-r acl

-r cat

-r cnt

-r coll

-r comm

-r dumpacl

-r query

-r sched

-r taxon

-s storeName

-t contentType

-v

Location

$BV1TO1/bin

Usage

This utility affects all running Interaction Manager servers running on all hosts, unless you limit the
set with the -a option.

Specify at least one of the -r options or the -e option. For example:

cache_utl -r cat -r cnt

To use the -c option to load a speciﬁc item into the cache, you must also include the -s, -t, and
-r cnt options. For example, to load the product whose PROD_ID is “922-6168C”:

cache_utl -s MyBank -r cnt -t PPRODUCT -c 922-6168C

To ﬂush a script cache:

cache_utl -e script_cache -d flush

The One-To-One servers must be running to run this utility.

BroadVision, Inc.

Installation and Administration Guide

See also

“Conﬁguring caching” on page 58, “imgr_acltool” on page 193, “tmpl_mgr” on page 198, and
“Changing the request cache dynamically” on page 121.

Chapter 9 Utilities and other files
dump_taxon

193

dump_taxon

This utility reads the categories and matching attributes from the Content tables, and compiles the
information into a cache ﬁle that the Interaction Manager can use for fast matching.

Syntax

dump_taxon

Location

$BV1TO1/bin

Usage

This utility takes no arguments. When run, it writes a cache ﬁle named taxon to the
$BV1TO1_VAR/cache directory. To load the cache information into the Interaction Manager’s
cache, use cache_utl, described on page 191.

See also

“cache_utl” on page 191.

imgr_acltool

Reports the access control speciﬁcations for an access control ﬁle belonging to an Interaction
Manager application. Can be run interactively or speciﬁcally. This utility is a wrapper for the acltool
utility that is speciﬁc to Interaction Manager application access. It always uses the default ACL ﬁle
for an application, and contains an additional command to refresh the access control cache.

Syntax

imgr_acltool [-A applicationName ] [ command argumentList ]

Location

$BV1TO1/bin

Usage

This utility is similar to acltool except that it does not support the load command. Instead, this
utility always loads the speciﬁcations from the access control ﬁle speciﬁed in the Interaction
Manager conﬁguration ﬁle, usually /etc/opt/BVSNsmgr/bvsm.cfg. [See “bvsm.cfg” on page 190 for
more information about the Interaction Manager conﬁguration ﬁle.]

The imgr_acltool utility provides an additional command, refreshcache, to refresh the access
control speciﬁcations cached by the Interaction Manager. The refreshcache command calls the
cache_utl utility to refresh the access control manager cache. If you just want to refresh the cache,
consider using cache_utl directly. [See “cache_utl” on page 191 for details.] For example, to load the
access control ﬁle for an application named Broadway:

imgr_acltool -A Broadway refreshcache

See also

“acltool” on page 158, and “cache_utl” on page 191.

Installation and Administration Guide

BroadVision, Inc.

194

Chapter 9 Utilities and other files
imgr_conf

imgr_conf

The utility provides an interface to the Interaction Manager. With this utility, you can start or stop
the Interaction Manager, or edit the Interaction Manager’s conﬁguration ﬁle.

Syntax

imgr_conf [ [-a action] [-p path]

[-A appName] (UNIX)
[-n appName] (Windows NT)
[-s scriptLibDirectory] [-t sessionTimeout]

| [-h] [-u] ]

-a action

Speciﬁes the action to perform. Valid actions are:

• start — Starts one or more Interaction Managers. How many it starts is

dependent on the engines setting in the conﬁguration ﬁle. This is the default
activity for imgr_conf.

• stop — Kills all running Interaction Managers.
• configure — Runs an interactive editor to edit the Interaction Manager’s

conﬁguration ﬁle /etc/opt/BVSNsmgr/bvsm.cfg. This option prompts for
conﬁguration settings, and suggests reasonable default values. [See“Conﬁguring
the Interaction Manager server” on page40 for details.]

-A appName
(UNIX only)

Interaction Manger installation name to conﬁgure. [See“Named applications” on
page104 for details.]

-h

Displays the syntax usage message.

-n appName
(Windows NT only)

Interaction Manger installation name to conﬁgure. [See“Named applications” on
page104 for details.]

-p path

Speciﬁes full path (must begin with “/”) to the Interaction Manager’s executable ﬁle.
Use this to override the default, which is $BV1TO1/bin/bvsmgr

-s scriptLibDirect

Identiﬁes directories containing start-up scripts to load into the Interaction Manager
script-cache when the server starts. script_lib_dir is a colon-separated string of
directory names that each contain start-up scripts. Any foreign objects in these
directories will cause initialization to fail, and the Interaction Manager won’t be able
to execute any scripts.

-t sessionTimeout Speciﬁes the how long (in minutes) a visitor’s session can remain inactive before the
Interaction Manager automatically logs the visitor out. This option takes precedence
over the value speciﬁed in the conﬁguration ﬁle.

Warning, in the future this option will not be supported. Use the conﬁguration ﬁle
instead.

-u

Displays the syntax usage message.

Location

$BV1TO1/bin/

Usage

Both the $BV1TO1 and $BV1TO1_VAR environment variables must be set to run this utility.

If you omit all arguments, imgr_conf starts up the Interaction Managers speciﬁed in the
bvsm.cfg conﬁguration ﬁle.

If you modify the configuration to change the count of Interaction Manager engines, you must
restart the HTTP servers for them recognize the new configuration.

BroadVision, Inc.

Installation and Administration Guide

Chapter 9 Utilities and other files
indexer

195

indexer

Builds Verity search collections that contain the indexes that Verity uses to perform full-text and
ﬁeld searches for content and external ﬁles.

Syntax

indexer [ options ] ...

-A appName

-about

-b

Interaction Manager application name. Use this option when the Interaction
Manager script root directory is that same as the HTTP server’s doc root
directory. The indexer uses the script root directory location obtained from
the bvsm.cfg ﬁle as the directory that contains external documents to index.

Use either -A or -r, but not both. If you omit both, the indexer uses the
directory in /etc/opt/BVSNsmgr/bvsm.cfg on the current host
machine.

Show the descriptive text for the collection as deﬁned by the
-description option when the collection was created.

Rebuild the index. Use this option after content has been deleted, or
periodically to balance the index. If you omit this option, the index only adds
new or modiﬁed content information to the index.

-c contentID

Content type ID.

-collection collectionName Name of the collection to index or reindex. The collection name should be in

-content_name
contentName

-d directory

the form serviceName_contentName, and by default, should be
located in the $BV1TO1_VAR/collection/ directory. The complete
path to the ﬁle is the location that must be passed to the search system API
when a function makes the search request.

Name of the content type to index. Must be one of the names deﬁned in the
database schema, such as PRODUCT or EDITORIAL. If you omit this
option, the indexer assumes EDITORIAL.

Directory where the Verity common directory is located. It should be
$BV1TO1/verity/common, which is its default location. Note that the
directory must be in the $PATH, and the Verity shared library
libvdk200.so must be in the $LD_LIBRARY_PATH path.

-description textDescription Descriptive text about a collection that can later be retrieved with the

-about option. See the Verity documentation for details.

-dir_ﬁles

-exclude_cat ﬁlename

-f ﬁlename

Index external ﬁles in speciﬁed directories. When this ﬂag is included, the
indexer indexes all ﬁles in the directory speciﬁed by FILE_PATH attributes
that have an asterisk (*) wildcard for the ﬁlename, such as
/APIRef/*. [See“Indexing directories” on page90 for details.]

File containing categories to be excluded. Content in the excluded
categories will not be indexed, and therefore not found by searches. You
can only specify this or -include, but not both. [See“Excluding content”
on page90 for details.]

Attribute mapping ﬁle. This ﬁle identiﬁes which attribute can be ﬁeld or full-
text searched. If you omit this option, the indexer treats all TEXT, STRING,
and FILE_PATH attributes as full-text searchable, and does not provide
ﬁeld-search for the table. [See“Attribute mappings ﬁle” on page88 for
details.]

-help

Displays summary information about program usage.

-include_cat ﬁlename

File containing categories to be included. You can only specify this or
-exclude, but not both. [See“Excluding content” on page90 for details.]

Installation and Administration Guide

BroadVision, Inc.

196

Chapter 9 Utilities and other files
indexer

-r docRootDirectory

-s serviceID

-service_name
serviceName

-style styleDdirectory

-t tempDirectory

-v messageLevel

HTTP server document root that contains external ﬁles to index. If you omit
this option, the indexer assumes -A. Use either -A or -r, but not both.

Service (store) ID that owns the content to index.

Service (store) name that owns the content to index.

Directory that contains the style ﬁles that deﬁne the Verity tables and ﬁlters.
By default, this is $BV1TO1/collection/style. [See“Field
deﬁnitions” on page87 for information about style ﬁles.]

Temporary directory that the indexer uses to dump tables for indexing
purposes. By default, this is $BV1TO1/collection/tmp. This directory
must have sufﬁcient space to hold the dumped content table.

Message verbosity level. Level 0 prints only error messages, while level 1,
the default, prints some informational messages.

Location

$BV1TO1/bin/

Usage

Running the indexer with no arguments creates a full-text searchable index of the Editorial TEXT,
STRING, and FILE_PATH attributes. The location of the external ﬁles identiﬁed by the FILE_PATH
attributes is the script root deﬁned in the /etc/opt/BVSNsmgr/bvsm.cfg ﬁle on the current host
machine. It also only looks at content that belongs to the service whose ID is zero (0), which is often,
but not guaranteed to be the default service for your site.

% $BV1TO1/bin/indexer

If the collection does not exist for the content, indexer creates one. But, by default, if the ﬁle does
exist, indexer only updates the collection with information from new and modiﬁed content and
ﬁles. To force it to rebuild the index, which is essential after deleting content, include the -b ﬂag.

% $BV1TO1/bin/indexer -b

To identify a different location for the HTTP server’s document root directory, either use the -r
option and specify the full path to the location, or use -A to identify an Interaction Manager
conﬁguration ﬁle whose script root is the same as the document root directory. For example, to use
-r and index the Editorial content that belongs to the MyBank service:

% indexer -service_name MyBank -r /docroot/filepath -b

See “External files” on page 89 for restrictions and more information about the document root
location. And see “Indexing directories” on page 90 for instructions for indexing all the files in a
directory reference by a content item.

To index something other than Editorial content, you need to deﬁne the style ﬁles for the content,
and then name the content with the -content_name argument. By default, One-To-One provides
style ﬁles for Editorial and Product content, and the ﬁles are located in the
$BV1TO1_VAR/common/style directory.

% indexer -service_name MyBank -content_name PRODUCT \

-r /docroot/filepath -b

BroadVision, Inc.

Installation and Administration Guide

Chapter 9 Utilities and other files
load_data

197

To take advantage of the ﬁeld-search capabilities, you have to identify an attribute mapping ﬁle that
associates content attributes with Verity ﬁelds. For information about these ﬁles and how they work,
see “Utilities and other ﬁles” on page 157. To tell indexer which mapping ﬁle to use, include the -f
argument:

indexer -service_name MyBank

-f filepath/prodMapFile \

-content_name PRODUCT -r /docroot/filepath -b

To eliminate content items as searchable content, identify the categories of items to exclude by
deﬁning them in a ﬁle, and naming that ﬁle as the -exclude_cat argument. [See “Excluding
content” on page 90 for details about the ﬁle.] To run the indexer and exclude the categories named in
the product_excludes.dat ﬁle:

indexer -service_name MyBank -content_name PRODUCT \
-exclude_cat product_excludes.dat \
-r /docroot/filepath -f filepath/prodMapFile -b

You can also identify categories to include with the -include_cat option. However, you can use
either -include_cat or -exclude_cat, but not both.

See also

See “Using the Verity search engine” on page 86 for complete information about conﬁguring and
using the Verity search feature.

load_data

This utility Broadway sample application data into the One-To-One database. See “Conﬁguring the
Broadway sample application” on page 50 for details about using this utility.

Note that this utility stops and restarts the One-To-One servers as part of its operation.

migr_coll

Migrates matching rule collections: matching rules that return categories, rather than content.

Syntax

migr_coll

Location

$BV1TO1/bin/

Usage

Run this utility while the One-To-One servers are running. It searches the database and updates the
collections for every service deﬁned in the bv1to1.conf conﬁguration ﬁle. While its running, it
reports which services it updated. For example:

% migr_coll
Processing store_id = 0
Processing store_id = 90
Finished processing all stores!

Installation and Administration Guide

BroadVision, Inc.

198

Chapter 9 Utilities and other files
migrate_to_v3.0

migrate_to_v3.0

Migrates One-To-One Version 2.6 database tables to the Version 3.0 schemas.

Syntax

migrate_to_v3.0 [ server database databaseUser databasePassword ]

Location

$BV1TO1/bin/scripts/loader/

migrate_to_v4.0

Migrates One-To-One Version 3.0 database tables to the Version 4.1 schemas.

Syntax

migrate_to_v4.0 [ server database databaseUser databasePassword ]

Location

$BV1TO1/bin/scripts/loader/

migrate_to_v4.1

Syntax

migrate_to_v4.1 [ server database databaseUser databasePassword ]

Location

$BV1TO1/bin/scripts/loader/

Usage

See “Upgrading to Version 4.1” on page 17 for instructions for using this utility.

tmpl_mgr

This utility controls the Interaction Manager’s page template caching mechanism.

The cache_utl utility manages all other caches. See “cache_utl” on page 191 for details.

Syntax

tmpl_mgr [ options ]

-a appName

-b

-c

Identiﬁes a named Interaction Manager. If you omit this option, the utility affects
all running Interaction Managers, as speciﬁed by the bvsm.cfg conﬁguration
ﬁle. [See“Named applications” on page104 for more information about
Interaction Manager names.]

Block (suspend) HTTP request thread execution. Any pending and new
requests remain in the Interaction Manager HTTP request queue. Note, all
browsers currently connecting to the site will appear to “hang” until request
processing resumes.

Continue (resume) HTTP request thread execution.

BroadVision, Inc.

Installation and Administration Guide

Chapter 9 Utilities and other files
tmpl_mgr

199

-d

-e

-l

-p

Disables caching and purges the cache.

Enables caching.

Lists all cached page templates. This is the default behavior if you omit all
options.

Purges all page templates from the cache.

-r template

Removes the speciﬁed page template from the cache.

-s

Shows the IDL requests that are pending in the Interaction Manager IDL
request queue. These are administrative requests — such as cache ﬂushing —
that have not yet been executed.

-?/h/H

Displays the usage message.

Location

$BV1TO1/bin/tmpl_mgr

Usage

When you start the Interaction Manager, by default it caches page templates and uses the cached
version for subsequent requests for a page. In a development environment, you will want to either
disable the cache, or periodically purge the cache to force the Interaction Manager to read the
updated page template. If you omit all options, this utility defaults to the -l option, list the cached
pages. It also displays the usage message.

Installation and Administration Guide

BroadVision, Inc.

200

Chapter 9 Utilities and other files
watcher

watcher

Allows you to monitor the state of your Interaction Managers, and automatically restarts any that
are found to be not running.

Syntax

watcher [ -a appName ]

-a appName

Interaction Manager installation name to conﬁgure. [See“Named applications” on
page104 for details.]

Location

$BV1TO1/bin/

Usage

You can monitor the default installation by running watcher with no command-line arguments:

% watcher

Or, to watch another installation, use the -a option and specify the installation’s application name:

% watcher -a appName

The watcher utility checks for expired Interaction Managers at a frequency deﬁned by the
engine-check-interval parameter in the Interaction Manager conﬁguration ﬁle, bvsm.cfg,
which you edit by running imgr_conf -a configure.

Launch this program from a user account that has permission to launch Interaction Managers.
Additionally, it must be run with the same environment used to install and start Interaction
Managers. The safest way to do this is to source the appropriate shell script,
$BV1TO1_VAR/etc/bv1to1.conf.csh or …/bv1to1.conf.sh, before launching the program
[see the “Shell start-up scripts” on page 39].

For more information about using this utility, see “Monitoring for dead Interaction Manager
servers” on page 155

BroadVision, Inc.

Installation and Administration Guide

A Component and dynamic object

shared libraries on Solaris

201

Solaris supports the concept of versioning of a .so ﬁles to provide a means to automatically detect
when an incorrect library version is being loaded. One-To-One supports versioning of the shared
object libraries so that version mismatches can be caught by the run time linker — each ﬁle is set up
with dependencies on a particular version. This applies to the shared libraries that contain
component object and dynamic object implementations.

This affects component objects and dynamic objects in two ways:

l When you build a library consisting of your objects, the library name should be libXXX.so.N
where XXX is the name of the library and N is the version number. Place libXXX.so.N in the
directory where the Interaction Manager’s stores its component and dynamic object libraries.
See “Conﬁguring the Interaction Manager server” on page 40 for more information.

l You should generate a symbolic link (ln -s) named libXXX.so in that same directory, with the
link contents being ./libXXX.so.N. The Solaris loader is smart enough to ignore the link if it
points to the same ﬁle i-node as the *.so.N ﬁle. Previous versions used a hard link instead of
a soft link, and the linker assumed there were two different libraries instead of one. This caused
problems with double-loading of objects.

The ﬁle with the version number is the one that gets loaded, while the ﬁle without the version
number is needed in case other objects in other libraries depend on objects in the given library.

To build your own library with the correct version number embedded in the .so.1 data, use the -h
compiler option:

$ CC -o libfoo.so.1 -h libfoo.so.1 .....

Then create a symbolic link from libfoo.so to libfoo.so.1. Now when another library
depends on this library, such as

$ CC -o libbar.so.1 ..... -lfoo

The linker (ld) sees -lfoo and expands it to libfoo.so (which is a symbolic link to
libfoo.so.1). It then looks inside of libfoo.so for its SONAME which is libfoo.so.1 and
creates a dependency on this inside of libbar.so.1 (To see the results, do a dump -Lv <obj>
and look at NEEDED). When the runtime linker (rtld) builds the image for an executable to run, it
looks at all the NEEDED recursively and uses LD_LIBRARY_PATH and RUNPATH to ﬁnd all the
versioned objects. (See the Solaris Software Development Answerbook’s Linkers and Libraries Guide
for detailed information.)

Different releases of the same shared object library can have different version numbers. (For more
details on how versioning is implemented in Solaris, see the Solaris CC man pages for the -h
option.) By default, the One-To-One system installation creates the links for the shared libraries that
it installs, See the directory for examples.

Installation and Administration Guide

BroadVision, Inc.

202

Appendix A Component and dynamic object shared libraries on Solaris

BroadVision, Inc.

Installation and Administration Guide

Index

203

A

access control
cache 192
configuration file 189
configuring 55
processing order 56

configuring 55
performance issue 57
permission 55
permission list 55
specifications, reporting 158
specifications, reporting (interactive) 193
subject 55
subject item 57
visitor classifier 56
wildcards 57

accessors

defining external 68
tuning for performance 153

account, One-To-One 38
.ACL file 55
acltool utility 158
adm_srv server 171
admindb file 140
agencydb_path parameter 166
alert notifications 69
algorithm, matching 82
@ALL visitor classifier 56
@all visitor classifier 56
allow_multiple_feedback parameter 169
aname.exe gateway application 105
anamecgi gateway application 105
application name
"bvsm" 44, 45
default 44, 45

applications

files, placement and location of 57
migrating 28
apply_sql utility 157
attribute mapping file (Verity) 88
attributes

default rating range 82
maximum rating range 82
rating ranges 81
ratings, how stored 82
authorizing payments 130
AVP Taxware 9

configuring 126
environment variables 126
installing 124
log file 126
$AVPAUDIT 126
$AVPIN 126
$AVPOUT 126
$AVPTEMP 126

B

back-end machines 149
backup procedures 141
base directory, see $BV1TO1
binary matching algorithm 82

effect of negative values 83

bounced_email_utl utility 160
BroadVision, contacting xi
Broadway sample application 50

bw_star.html file 52
search fails 52
service name requirement 37
Verity collections 52
BV_ALERT_INBOX table 73
BV_ALERTSCHED table 70
BV_ALERTSTAT table 78
BV_CacheControl namespace object 99
bv_check_want_message_attr parameter 73
bv_database parameter 67
$BV_DB_DATABASE 33
$BV_DB_LIB variable 67
$BV_DB_LIB_PATH variable 67
bv_db_passwd parameter 67
$BV_DB_SERVER 33

Installation and Administration Guide

BroadVision, Inc.

204

Index

$BV_DB_USER 33

must match $ORACLE_SID 164

$BV_DB_VENDOR 33, 163
bv_dbserver parameter 67
bv_dbuser parameter 67
bv_dcc_document_root parameter 169
bv_dcc_schedule_root parameter 73
bv_dcc_script_root parameter 169
bv_dcc_template_root parameter 169
bv_email_host parameter 77
BV_GenericCacheMgr::set_default_cache_size() 121
BV_INVOICE_CONFIRMATION_TABLE table 128
bv_js_library_dir parameter 73, 166
BV_LC_LIST parameter 63

setting 64

BV_LC_MONEY parameter 63
$BV_LD_LIBRARY_PATH variable 165
bv_load_content utility 157
bv_load_users utility 157
bv_make_money(), currency formatting 64
BV_MSGSCHED table 70
BV_MSGSCRIPT table 73

SCRIPT_FORM column 73
SCRIPT_TXT column 73

BV_MSGSTAT table 78
$BV_ORB_BIDIRECTIONAL_IIOP 163
$BV_ORB_CALL_TIMEOUT 164
$BV_ORB_CONNECT_TIMEOUT 164
$BV_ORB_DIAGNOSTICS 164
$BV_PATH variable 165
BV_PROFILE_TAXON table 81
$BV_RSH_PATH 165
bv_schedule_keep_messages parameter 74
bv_schedule_msg_dir
directory 70
parameter 71

bv_schedule_script_root parameter 73
bv_schedule_startup_root parameter 73
bv_schedule_static_msgcount parameter 74
bv_site_id
file 92
setting 91

BV_SRV_STAT memory option 148
BV_STORE table 172
BV_USER table

USER_ALIAS attribute 56

BV_USER_PROFILE table

e-mail address attribute 74
INVALID_EMAIL flag 160
WANT_MESSAGE attribute 73

BV_USER_ROLE table

USER_ROLE attribute 56
BV_Y2K_CUTOFF parameter 61
$BV1TO1 32

as root directory 4
directory cloning 94

HP-UX 13
Solaris 11
Wiindows NT 15

bv1to1.conf file 161
updating 37

bv1to1.conf.delta file 176
bv1to1.conf.o file 176
$BV1TO1_INSTANCE 92
$BV1TO1_ROOT_HOST 163
$BV1TO1_VAR 32

mutiple installations 93

bvconf monitor

report options 148

bvconf utility 174
bvconf_srv server 171
bvensapi.sl library 44, 105
bvensapi.so library 44, 105
bvensapi3.sl library 44, 105
bvensapi3.so library 44, 105
BVI_Visitor.visitorByID(), interface change 27
bvisapi.dll library 105
bvkill utility 183
bvlog utility 183
.bvlog.conf configuration file 184
bvlog.YYMMDD file 80
bvobs.conf configuration file 187
bvobs.out.YYMMDD file 80
bvping utility 188
bvsm.ACL file 189
syntax 55

bvsm.ACL.default file 55
bvsm.bvisapi.<processId> file 47
bvsm.cfg configuration file 190
bvsm.inetcgi.<processId> file 49, 50
bvsm.nsapi.<processId> file 45
bvsm.req configuration file 114, 191
bvsm.startup.log 155
bvsm_version utility 191
bvsmgr_0.cfg configuration file 155
BVSNcgi_logs

directory 154
file 49

BVSNsmgr directory 41
BVSNsmgr_logs directory 154
bw_start.html file 52

C

cache 58

access control 192
content, cache size limits 60
firewalls, and 58
generic database 59
guidelines 60

BroadVision, Inc.

Installation and Administration Guide

Index

205

manipulating 191
page templates 198
pages, what can be cached 113
request cache 192

configuration file 114
configuring 113
flushing 121
monitoring 122
name 121

request configuration file 191
scripts 192
turning off 59
cache_utl utility 191
cachecontrol_path parameter 99
cat_cache_size parameter 60
category

caching 60
null 54

CD-ROM mounting
HP-UX 12
Solaris 10

CGI

gateway configuration 48
log files 49
running multiple applications 111
when to use 43

character sets 65

charset HTTP setting 65
database 34
European SQL Server 65
Informix 36
Interaction Manager 65
Oracle 65
Sybase 35

characters

encoding for Command Center 169
reserved 163

charset HTTP setting 65
$CLIENT_LOCALE 36
cmsdb server 171
tunning 149

cmsdb_path parameter 167
cnt_cache_sizes setting 59
cnt_type_cache_size setting 59
cntdb server 171

tuning 149

cntdb_path parameter 167
collections (content)
cache size 59
migrating 25

collections (search)
creating 89
directory (Verity) 87

Command Center

can’t connect to server 8
character encoding 169

character formatting 62
currency code 63

“CommandCenter” group name 172
commerce configurations 123
common directory (Verity) 87
community visitor classifier 56
components

libraries 165
library directory 26
migrating 28
shared object libraries 201

concepts of One-To-One 4
configuration

activities 101
changing at runtime 168
commerce activities 123
concepts 4
files 157

locations of 2
migrating 37
multiple installations 93
One-To-One 161
for initial start-up 31
hardware configuration 150
managment server 171
One-To-One 37
server activities 53
terms 4

content

accessor (database) 66
cache, setting size of 59
chaching 59
database server 171
rating values 81
unclassified, changing the label of 54

control file 55
CPU performance 149
crash recovery 140
ctxdriver utility 157
currency

Command Center symbol 63
euro and country-specific locales 64
format 62

custom payment handler 130

D

daily_quote.jsp file 27
data cache

See cache

database

access password 176
accessors

configuring 66

Installation and Administration Guide

BroadVision, Inc.

206

Index

performance issues 153
statistics 147
tuning for performance 153

back ups 141
cache, generic 59
configuring 3
corruption recovery 144
corruption, avoiding 8, 9
idle reconnect time 67
migration 21
password 162, 176
server crash recovery 143
sharing between servers 92
sharing in a multiple-site configuration 95

documentation

HTML format x
PDF format x
related x

Domain Name Server, See DNS
dual-homed hosts 107
dump, bvconf command 175
dump_taxon utility 193
Dynamic Objects
libraries 165
library directory 26
migrating 28
shared object libraries 201

database parameter 67, 167
date/time format 62
dates

changing rule evaluation time 86
overriding the system date-time 86

$DB_LOCALE 36
DBCENTURY Informix setting 36
DBLANG parameter 36
dblib parameter 67, 167
$DBMONEY

currency setting 64
Informix German 36

DBMS

environment variables 33
permissions, account 33
dbserver parameter 67, 167
dbuser parameter 67, 167
default service 54
default_city parameter 127
default_cnt_cache_size setting 59
default_country parameter 127
default_locality parameter 127
default_pmt_methods parameter 132
default_postal_code parameter 127
default_service parameter 54
default_setup.reg script 47
deliv_comp_d daemon 171
deliv_comp_d daemone
configuring 78

deliv_smtp_d daemon 171

configuring 76

delivery completion server 78
delivery server, e-mail 76
deny access permission 55
destination, default address 127
development system 93
diagnostic parameter 170
directories 2
discdb_path parameter 167
discussion group messages, purging 156
DNS 8
document root 4, 103

E

electronic credit card purchases 135
e-mail

address visitor profile column 74
delivery server 76
flag, updating for invalid 160
messages 69

encoding_type parameter 65, 169
engine-check-interval parameter 200
environment variables 163

accessing from page scripts 31
database 33
Informix 36
Oracle 33
setting 31
site-specific, adding to configuration 39
start-up scripts 39
Sybase 35
system 32

errors

125: Address already in use 110
Bind retry failed 110
can’t connect to server 8
Couldn’t initialize INETListener 110
database corruption, avoiding 8
Interaction Manager 154
logging messages 184
machine crash 140
ORA-04031: unable to allocate 34
Stored procedure initialization Error 1 58

euro, country-specific locale and euro 64
European locales, SQL Server character conversion 65
execute, bvconf command 175
export variables 163
ext_accmethod parameter 68
ext_datasource parameter 68
ext_dbname parameter 68
ext_dbpassword parameter 68

example 67

BroadVision, Inc.

Installation and Administration Guide

ext_dbserver parameter 69
ext_dbtype parameter 68
ext_dbuser parameter 69
ext_lib parameter 69
ext_writeprotect parameter 69
extdbacc server 171
external accessors 66
defining 68

external database password 68
external_content_write parameter 68
external_profile_write parameter 68

F

field-search 87
firewalls 106

caches, and 107
definition 4
hardware configuration 150

fix up scripts 115
flat tax 126
flush_one_content() 61
front-end machines 149
front-line servers 96
full-text search 87

G

gateway applications 105
configuration file 190

gateway configuration

CGI 48
IIS 46
NES 44

gateways 102

session IDs, and 106

gdb_query_cache_size parameter 59
gdb_query_cache_timeout parameter 59
gdb_query_limit paramter 59
generic accessor 66
generic database cache 59
genericdb server 171
German currency symbol 64
get_attr.sql script 58
group, CommandCenter 172
@GUEST visitor classifier 56
@guest visitor classifier 56

H

hardware configuration 150

Index

207

help, bvconf command 177
host

definition 4
multiple 170
parameter 170
remote shell command 165
replacing 143

host machines 1

dual homed 107

hostmgr server 171
HTML character sets 65
HTML One-To-One documention x
HTTP servers

character sets 65
directories 103
Interaction Manager interaction 102
migrating 26
performance issues 152
ports for multiple Interaction Managers 104

HTTPS, using 112

I

ignore_cache_limit parameter 60
IIS 46

gateway configuration 46
log files 47

imgr_acltool utility 193
imgr_conf utility 194
inbox, visitor 69
incndb_path parameter 167
indexer utility 195
using 89
inetcgi gateway

migrating 26

inetcgi gateway application 105

migrating 26
using 48

inetcgi.exe gateway application 105
Informix

character set 36
environment variables 36

$INFORMIXDIR 36
$INFORMIXSERVER 36
initial_user_profile_attrs parameter 58
INSTALL (HP-UX) script, running 12
install (Solaris) script, running 11
install_observe_db utility 157
installing 10

One-To-One 7
concepts 4
HP-UX, on 12
prerequisites 8
rehearsal installation

Installation and Administration Guide

BroadVision, Inc.

208

Index

Solaris 11
Solaris, on 10
terms 4

instance name, server 92
Interaction Manager 40

cache 191
configuration errors 154
configuration file 190
configuring 40
error files 154
firewalls, configuring for 106
gateways and session IDs 106
HTTP server interaction 102
inetcgi gateway 48
interface utility 194
IP masking 111
log files 154
migrating 26
multiple from one CGI host 111
named applcations 104
page template cache 198
performance tuning 151
ports and IP addresses 108
proxy servers, adjusting for 111
remote host configurations 107
request cache configuration file 191
servers, isolating 93
starting 42
statistics 147
stopping 138
trouble shooting 49
verifying running server 188
version, retrieving 191
international currency format 62
INTL_CURRENCY parameter 63
intl_currency parameter 63, 169
INTL_PRECISION parameter 63
INVALID_EMAIL flag 160
invoice destination 127
invoice taxing 126
IP address, multiple on one machine 107
IP addresses

Interaction Manager 108

IP masking 111
ISAPI

see also IIS
when to use 43
ISOCharset parameter 66
$IT_DAEMON_PORT 32
IT_DAEMON_SERVER_BASE parameter 164
IT_DAEMON_SERVER_RANGE parameter 164

J

jsic utility 157

L

LANG environmnet setting 63
languages (locale)

changing for an installation 62

launch servers 178

bvping, using 188

LC_ALL environmnet setting 63
LC_COLLATE environmnet setting 62
LC_MONETARY environmnet setting 63
LC_TIME setting 63
$LD_LIBRARY_PATH envionment variable 22
LD_LIBRARY_PATH environment setting 39
libclntsh.so shared library 33
libraries

component 165
Dynamic Object 165

line-item

destinations 127
taxing 126
load balancing 170
load_data utility 197

using 51

load_v2cat utility 157
load_v2cnt utility 157
locales 62

currency format 62

log files

backing up 141
bvlog.YYMMDD 80
bvobs.out.YYMMDD 80
BVSNcgi_logs 49
configuring 184
debugging, for 143
error messages 184
Interaction Manager 154
messages improving performance 95
microtransactions

configuring 129
directory for 129
mtlog.YYMMDD file 129
observations

configuring 80
directory for 80

Orbix connection errors 154
output 186
payment handling 135
pmtlog.YYMMDD 135
taxaulpf 126
truncating 141

BroadVision, Inc.

Installation and Administration Guide

See also the Database Administrator’s Guide

log_sig parameter 168

migrate_to_v4.1 utility 198
migrating 17

Index

209

M

machine crash 140

recovery 143

machines 1
maintaining stand-by servers 142
maintenance

activities 137
back ups 141
crash recovery 140
database server crash recovery 143
Omnihost crash recovery 144

map_store_user utility 157
match_cat_preload parameter 60
matching

adding input argument to Matching Agent dialog 85
algorithm 82

effect of negative values 83

attributes 81
configuring 81
cutoff percentage 83
cutoffs 83
database values 81
default algorithm 82
maximum score 83, 84
rankings 83
rules

cache, setting size of 59
migrating 25
testing 86

sort order, content 84

Matching Agent 81
configuring 81
dialog input arguments 85
max_idle_time parameter 67, 167
maximum matching score, overriding 84
McAfee VirusScan 38
messages (discussio groups), purging 156
messages (Notification) 73
directory tree 71
scripts 73
targeted 69

messages (system), logging 184
meta data 3
Microsoft Internet Information Server

see IIS

microtransaction, logging 129
migr_coll utility 197
migrate_to_v3.0 utility 198
migrate_to_v4.0 utility 198

using 22

applications 28
components 28
configuration settings 37
database 21
Dynamic Objects 28
HTTP server 26
Interaction Manager 26
matching rules 25
prerequisites 19
scripts 27
system configuration 23

mime-types file 44
MKS Toolkit

installation 14

monitor, bvconf command 177
monitoring

database accessor statistics 147
Interaction Manager statistics 147
server processes 145
statistics 146

msg_not_completed directory 70
mtlog.YYMMDD file 129
multiple-site configuration 95
mxt_load utility 157

N

name space objects, updating 98
named applications 104
NES

gateway configuration 44
log files 45
tuning for performance 152
when to use 43

Netscape Enterprise Server

see NES

Netscape SSL servers 112
networks, multiple on one host 107
NLS_LANG parameter 65
$NLSPATH 164
$noecho function 67
notification process 70
notifications 69

configuring 69
daemons 74
delivery completion server 78
delivery server, e-mail 76
message directory tree 71
messages 73
processes (servers) 74
schedule poller 74
schedule server 75

Installation and Administration Guide

BroadVision, Inc.

210

Index

ns, bvconf command 177
NSAPI

see NES

nsloader.log log file 45
null_category setting 54
num_cnt_cache setting 59

O

obj.conf file 44
obs_aggr utility 157
obs_dbload utility 157
observation logging

SQL Server access permissions 35

observation_flag parameter 80
observation_flush_time parameter 80
observations

error files 80
logging 80
reports 80

of_path parameter 167
ofbe_path parameter 167
ofbe_srv server 171
ofdb server 171
ofdb_path parameter 167
OID 91
om_srv server 171
Omnihost payment handling system

configuration file 135
crash recovery 144
version 9

omnihost.cfg file 135
One-To-One

account 38
backing up 141
checking servers 188
concepts 4
crash recovery 140
installing 10

HP-UX, on 12
Solaris, on 10

interface utility 174
meta data 3
multiple host installations 93
multiple installations 92
multiple sites with one database 95
prerequisites 8
removing 15
restarting 139
root directory 4, 15
running multiple on same machine
see $IT_DAEMON_PORT

shutting down 138
starting 38

upgrading from older version 17
user account 38

optimized binary matching algorithm 82

effect of negative values 83
$ORA_NLS in bv1to1.conf 164
Oracle

character set 65
environment variables 33
Oracle 8, bad library 33
prerequisites 9
shared memory pool size 34
shared memory size 34
TNS_ADMIN parameter 33
tnsnames.ora file 33

$ORACLE_HOME 34
$ORACLE_SID, in bv1to1.conf 164
$ORACLE_TERM, in bv1to1.conf 164
ORB 32

port 32

Orbix

connection timeout control 164
object request broker

See ORB
test for active 49

orbix.log file 154
order numbers, changing the format 128

P

page template cache 198
pages, what can be cached 113
param_file parameter 135
password

database 162, 176
external database 68
parameter 67

password parameter 167
$PATH variable 165
payment

authorization 130
handler 130

configuring 131
logging 135
objects 130
handler, custom 130
methods 132
processing 130
settlement 130
types 130

configuring 131

PDF documentation x
perfmeter UNIX utility 151
performance tuning 149
cache tuning 58

BroadVision, Inc.

Installation and Administration Guide

HTTP servers 152
Interaction Managers 151
Netscape Enterprise Server 152
processos 153

permissions (access control) 55
permissions (database), DBMS account 33
ping, bvconf command 178
pmt_addr_from_profile 131
pmt_method parameter 133
pmt_methods parameter 132
pmt_type parameter 133
pmtassign_d daemon 133, 171
pmthdlr_d daemon 133, 171
pmtlog.YYMMDD file 135
pmtsettle_d daemon 133, 172
ports

firewalls, to open for 32
Interaction Manager 108
precheck, bvconf command 179
prerequisites, installation 8
pricing rules, testing 86
privacy_flag parameter 167
problem reporting xi
processes 1

defining 169
monitoring 145

by name 146

tuning for performance 153

production systems 93
profdb_path parameter 168
profile accessor 66
profile attributes, caching 58
proxy servers, adjusting for 111
ps, bvconf command 179
psit utility 49
purge_agg_obs utility 157
purge_messages utility 157
purge_messages.sql 156
purge_raw_obs utility 157

Q

queries, caching 59
query_cache_size parameter 59
query_cache_timeout parameter 59
query_limit parameter 59

R

rating

default ranges 82
maximum range 82

Index

211

values and ranges 81
values, content 81

record_content_feedback parameter 169
rehearsal installation

Solaris 11

related documentation x
remote host shell 165
remote shell 165
remote sites 95
removing One-To-One 15
replicating a site 95
reports, observations 80
.req file 114
request cache

configuration file 114, 191
configuring 113
fix up scripts 115
flushing 121
monitoring 122
name 121
rule syntax 118
rules 117

reserved characters 163
restart, bvconf command 181
restarting the site 139
restoring after a crash 140
Rogue Wave versions 8
role visitor classifier 56
root

directory, definition 4
host, definition 4

root directory 15
rule_cache_size parameter 59
rule_eval_time file 86
ruledb_path parameter 168
rules

migrating 25
testing 86

S

sample application 50
save_member_limit 60
sch_gen utility 157
sch_gen utility, library requirement 165
sched_header.jsp script 73
sched_poll_d daemon 172
sched_poll_d server 74
sched_srv daemon 172
sched_srv process 75
schedule poller 74
schedule server 75
scheduled messages
See Notifications

Installation and Administration Guide

BroadVision, Inc.

212

Index

script root 103
scripts

flushing from cache 192
message 73
migrating 27
One-To-One 157
See also start-up scripts
system variables, accessing 31
what can be cached 113

searching

directories 90
See also Verity
secure sockets layer 112
security

firewalls 150
issues 9
server processes 1
servers

checking and launching 188

bvconf, from 178

front-line 96
instances 92
isolating 93
list all configured 180
monitoring 145

service

adding, changing, or removing 54
definition of 4
name 54

session ID format, changing 112
session profile terms 78
session_terms file 140

using 79

set_default_cache_size() 121
settling payments 130
setup 29
/bin/sh 39
shared libraries, adding custom libs to library path 39
shared object libraries 201
shared_pool_size oracle parameter 34
shell

remote 165
reserved characters 163
/bin/sh 39
start-up scripts 39

ship_calc_mode parameter 127
shipping

costs 127
flat rate 127

SHLD_LIBRARY_PATH environment setting 39
$SHLIB_PATH envionment variable 22
shutdown parameter 170
shutdown, bvconf command 181
shutting down the site 138
signals to servers 168
simple tax 126

simple_ship_rate parameter 127
simple_tax_rate parameter 126
site

backup procedures 141
definition 4
ID, changing 91

site parameter

multiple site configuration, in a 97

sites

multiple-site configuration 95
remote 95
replicating 95
service

default for a site 54
smap, bvconf command 182
smgr_first_port_minimum parameter 110
*.so files 201
Solaris library versioning 201
SQL Server

access permissions 35
European character sets 65
prerequisites 9
variables 35

srfac_path parameter 168
SSL 112
stand-by servers 142
starting

Interaction Manager 42
One-To-One 38

start-up scripts 39
statistics, monitoring 146
stedb_path parameter 168
style files 88
style.ufl file 88
subject item, access control 57
subject, access control 55
swap UNIX utility 151
SYB_CHARSET parameter 35
$SYBASE 35
Sybase

character set 35
environment variables 35
syntax_check, bvconf command 183
system

configuration 101
migration 23

configuring commerce 123
configuring servers 53
crash 140
development 93
environment variables 31
files 93
maintenance 137
production 93
time, changing rule evaluation 86
version 156

BroadVision, Inc.

Installation and Administration Guide

T

targeted messages 69
tax_calc_mode parameter 126
taxaulpf AVP log file 126
taxaulpf file 126
taxing

flat tax rate 126
line-item basis 126
turning off 127

Taxing system, configuring 126
taxon_max_score, example 84
taxon_sort_order parameter 84
taxon_use_binary_val_for_cnt parameter 83
taxonomy 81
technical support xi
terminology 4
testing matching and pricing rules 86
time, changing rule evaluation time 86
tmpl_mgr utility 198
TNS_ADMIN parameter 33
tnsnames.ora Oracle file 33
top command for One-To-One processes 145
top UNIX command 151
tuning for performance 149
typographical conventions xi

U

unclassified content, label of 54
unexpected behavior 143
UNINSTAL (HP-UX) script 16
uninstall (Solaris) script 16
uninstalling One-To-One 15
universal resource location 102
updating the configuration settings 37
upgrading 17
URL 102
user account 38
user administration server 171
user name

environment variable 33
same for all hosts 31
user_session_terms setting 79
utilities 157

V

variables 163
Verifone Omnihost

See Omnihost

Verity

Index

213

attribute mapping file 88
collection directory 87
collections 52
collections, creating 89
common directory 87
configuring 86
content, excluding 90
external files, searching 89
field definitions 87
FIELD mappings 88
field-search 87
full-text search 87
index 87
index, updating 91
indexing directories 90
license 8, 86
style files 88
TEXT mappings 88

version

Interaction Manager 191
migrating from older 17
system determining 156

versioning of libraries 201
versions directory 156
VirusScan, McAfee 38
visitor

classier, access control 56
inbox 69
management attributes 58
permissions 55
profile attributes, caching 58

Visitor Feedback
settings 169
See also the Database Adminisrator’s Guide

Visitor managment database server 171
visitor notifications

See Notifications

voting, See Visitor Feedback

W

watcher utility 200
using 155

wildcards, access control 57

Y

Y2K handling 61
year 2000 handling 61

Installation and Administration Guide

BroadVision, Inc.

214

Index

BroadVision, Inc.

Installation and Administration Guide

