---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/SWINDON/Additional documentation/Installation and Adminstration Guide (Summer 1999 revision).pdf.md
tags: [retail, pwc, swindon, sap-retail, broadvision, coe, 1999]
project: retail
status: unprocessed
---

# Installation and Adminstration Guide (Summer 1999 revision).pdf

## Source
File: `Brain/raw/.extract/SWINDON/Additional documentation/Installation and Adminstration Guide (Summer 1999 revision).pdf.md`
Size: 533,859 bytes

## Raw content
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


## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
