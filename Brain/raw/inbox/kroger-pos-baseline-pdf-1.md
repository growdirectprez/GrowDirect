---
date: 2026-04-22
type: raw
source: _scratch-kroger/reference/Kroger POS Baseline.pdf.md
tags: [secure, secure, kroger, retail, client-implementation]
project: secure
status: unprocessed
---

# Kroger POS Baseline.pdf

## Source
File: `_scratch-kroger/reference/Kroger POS Baseline.pdf.md`
Size: 6,231 bytes

## Raw content
C:\Users\geoff\OneDrive\Documents\BaseLine

ID
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78

Task Name
Kroger Secure 3.5 SaaS Implementation

Project Administration

Sysrepublic ongoing Project Management
Kroger Project Management
On Site Kickoff / Operational Review
Agree Baseline Project Plan

Phase 1 Point of Sale Exception Based Reporting
Deploy Baseline Secure & External Data Feeds

Phase 1 POS Analysis

Point of Sale Analysis

Collect existing process guides, operation manuals
Identify Point of Sale Data Source & Modifications necessary for External Sharing
Provide Point of Sale Technical Specification
Establish SFTP for Data Sharing
Provide data format & sample for Point of Sale Tlog

External Data Feed Analysis (Source & Spec & Sample Data & Historical Availability)

Item Master Data Feed
Store Master Data Feed
Employee Master Data Feed

Estimate Kroger development effort for external feeds

Analysis complete
Ongoing POS Mapping Guidance
Phase 1 Functional Design

Secure Strategy Workshop
Define High Level workflow
Define Roles and Permissions
Identify Dashboard and Report Requirements

Phase 1 Technical Design

Define the Solution Architecture

Complete Capacity Planning Exercise
Develop Hardware specifications
Define Network & Connectivity Requirements
Define Kroger Data Transport & Load Mechanism

Document the Solution Architecture

Solution Overview
Point of Sale Tlog Feed
Master Data Feeds
Approve Phase 1 Design

Phase 1 Technical Design complete
Phase 1 Development

Develop Kroger Data Extracts

POS Tlog Extract
Master Data
Send Test Data for Development
Develop Secure Data Transforms

Develop Data Transport & Load Mechanism
Establish SFTP Connectivity
Point of Sale
Master Data Feeds
Configure System Alerts and Monitors

Phase 1 Development complete
Integration Test

Receive Tlog & Reference Data files via Production Method
End to End Test TLOG Load Process
End to End Test Other Data Feeds

Integration Test complete
Kroger POS Data Validation

Configure Secure Application & CRDM in QA
Data Loaded for Validation Workshop
Data Validation Workshop
Resolve Data Validation Issues / Retest

Sign off Data Validation
Production Infrastructure

Establish Kroger Tennant Network
Provision Production Database Storage
Provision Production Secure Servers
Install Secure Configure production

Production infrastructure setup complete
Performance Test

Allocate SAN storage for Production CRDM
Load CRDM with historical TLOG data
Performance Test infrastructure

Performance Test complete
Deploy Secure

Phase 1 Training
Load Data to Production Environment
Finalize UI Configuration / Reports

Exception Based Reporting POS Go Live

Resource Initials

SRPM
KITM
SRPM,SRTL,SRCS
KLPM,SRPM,KITM

KSME
KPOS
KPOS
KITN,SRTL
KPOS

KITD,KSME
KITD,KSME
KITD,KSME
KITD,KITM

KPOS

KLPA,KLPM,SRCS
KLPA,KLPM,SRCS
KLPA,KLPM,SRCS
KLPA,KLPM,SRCS

SRTL
SRTL
SRTL,KITN
SRTL
SRTL
SRTI
SRTL,SRD1
SRTL,SRD2
SRPM,KITM

KDEV
KITD
KITD

SRD1,SRD2
KITN,SRTL
SRD1
SRD2
SRD2

KITD
SRTL,SRD1,SRD2,KITD
SRTL,SRD1,SRD2,KITD

SRCS
SRTL
SRCS,KLPA,KLPM
SRTL,SRD1,SRD2,KLPA,KLPM
KLPM

SRTI
SRTI
SRTI
SRD1,SRD2

SRTI
SRTI
SRTI

SRCS,KLPA,KLPM
SRD1,SRD2
SRTL,SRD1,SRD2

Page 1

Duration

95.5 days
95.5 days
17 days
13 days
1 day
1 day
1 day
2 days

Finish
Start
Fri 5/25/18
Mon 1/8/18
100 days
Fri 5/25/18
Mon 1/8/18
100 days
Fri 5/25/18
Mon 1/8/18
100 days
Fri 5/25/18
Mon 1/8/18
100 days
Tue 1/9/18
2 days
Mon 1/8/18
Thu 1/11/18
2 days Wed 1/10/18
Fri 5/25/18
Fri 1/12/18
Fri 5/25/18
Fri 1/12/18
Mon 2/5/18
Fri 1/12/18
Tue 1/30/18
Fri 1/12/18
Fri 1/12/18
Fri 1/12/18
Fri 1/12/18
Fri 1/12/18
Thu 1/18/18
Mon 1/15/18
Tue 1/16/18
Mon 1/15/18
Tue 1/30/18
10 days Wed 1/17/18
Fri 2/2/18
3 days Wed 1/31/18
1 day Wed 1/31/18 Wed 1/31/18
Thu 2/1/18
1 day
Thu 2/1/18
Fri 2/2/18
1 day
Fri 2/2/18
Mon 2/5/18
1 day
Mon 2/5/18
Mon 2/5/18
0 days
Mon 2/5/18
Mon 3/26/18
35 days
Tue 2/6/18
Fri 2/9/18
5 days
Mon 2/5/18
Mon 2/5/18
0.5 days
Mon 2/5/18
Mon 2/5/18
0.5 days
Mon 2/5/18
Mon 2/5/18
1 day
Mon 2/5/18
Mon 2/5/18
5 days
Fri 2/9/18
Tue 2/6/18 Wed 2/28/18
16.5 days
Fri 2/16/18
Tue 2/6/18
8.5 days
Thu 2/8/18
Tue 2/6/18
3 days
Tue 2/13/18
Fri 2/9/18
3 days
0.5 days Wed 2/14/18 Wed 2/14/18
Fri 2/16/18
2 days Wed 2/14/18
Fri 2/16/18 Wed 2/28/18
8 days
Thu 2/22/18
Fri 2/16/18
4 days
Fri 2/16/18
Fri 2/23/18
5 days
3 days
Fri 2/23/18 Wed 2/28/18
0 days Wed 2/28/18 Wed 2/28/18
0 days Wed 2/28/18 Wed 2/28/18
30 days Wed 2/28/18 Wed 4/11/18
16 days Wed 2/28/18
Thu 3/22/18
15 days Wed 2/28/18 Wed 3/21/18
Wed 3/7/18
Thu 3/22/18
30 days Wed 2/28/18 Wed 4/11/18
Wed 3/7/18
Thu 3/8/18
30 days Wed 2/28/18 Wed 4/11/18
Tue 3/6/18
4 days Wed 2/28/18
5 days
Tue 3/13/18
Tue 3/6/18
0 days Wed 4/11/18 Wed 4/11/18
5 days Wed 4/11/18 Wed 4/18/18
Thu 4/12/18
1 day Wed 4/11/18
2 days
Mon 4/16/18
Thu 4/12/18
5 days Wed 4/11/18 Wed 4/18/18
0 days Wed 4/18/18 Wed 4/18/18
Fri 5/18/18
22 days Wed 4/18/18
Mon 4/23/18
3 days Wed 4/18/18
Tue 4/24/18
Mon 4/23/18
1 day
Fri 4/27/18
Tue 4/24/18
3 days
Fri 5/18/18
15 days
Fri 4/27/18
Fri 5/18/18
Fri 5/18/18
0 days
Wed 5/9/18
Fri 4/27/18
8 days
Mon 4/30/18
Fri 4/27/18
1 day
Wed 5/2/18
Mon 4/30/18
2 days
Fri 5/4/18
Wed 5/2/18
2 days
Wed 5/9/18
3 days
Fri 5/4/18
Wed 5/9/18
Wed 5/9/18
0 days
Fri 5/18/18
Wed 5/9/18
7 days
Thu 5/10/18
Wed 5/9/18
1 day
Tue 5/15/18
Thu 5/10/18
3 days
Fri 5/18/18
Tue 5/15/18
3 days
Fri 5/18/18
Fri 5/18/18
0 days
Fri 5/11/18
10 days
Fri 5/25/18
Fri 5/11/18 Wed 5/16/18
3 days
Fri 5/25/18
Fri 5/18/18
5 days
Fri 5/25/18
5 days
Fri 5/18/18
Fri 5/25/18
Fri 5/25/18
0 days

5 days Wed 2/28/18
1 day Wed 3/21/18

5 days Wed 2/28/18
Wed 3/7/18
1 day

Predecessors

%

0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
