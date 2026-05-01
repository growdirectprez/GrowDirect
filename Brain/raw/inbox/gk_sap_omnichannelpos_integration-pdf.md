---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/tier1-md/gk-pos/GK_SAP_OmnichannelPOS_Integration.pdf.md
tags: [canary, gk-pos, fujitsu, reference, benchmark, tier1-extract]
project: canary
status: unprocessed
---

# GK_SAP_OmnichannelPOS_Integration.pdf

## Source
File: `Brain/raw/.extract/tier1-md/gk-pos/GK_SAP_OmnichannelPOS_Integration.pdf.md`
Size: 31,591 bytes

## Raw content
PUBLIC

2023-06-07

SAP Omnichannel Point-of-Sale by GK,
integration with SAP Customer Activity
Repository, SAP S/4HANA and SAP S/4HANA
Cloud

THE BEST RUN

.

d
e
v
r
e
s
e
r
s
t
h
g
i
r

l
l

A

.
y
n
a
p
m
o
c
e
t
a

i
l

ffi
a
P
A
S
n
a
r
o
E
S
P
A
S
3
2
0
2
©

Content

1

2

3

3.1

3.2

3.3

3.4

3.5

3.6

4

4.1

4.2

5

5.1

5.2

5.3

6

6.1

Overview. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4

Installation. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5

Configuration. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6

First Step – Value Mapping in "Mapping LOGSYS to Target". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6

Second Step – Endpoint Configuration for the Integration Flow "SOAP-from-GK-to-SAP-XI-
WebServices". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7

Third Step – Configure the RFC Destination. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8

Optional – How do I know which identifier in the value mapping matches my desired Integration
Flow?. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10

Special Integration Flow "GK POSLog XSLT Mapping". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11

Optional – How to find the correct URLs for an Integration Flow configuration?. . . . . . . . . . . . . . . . . 11

Explanation – Data Flow Diagrams. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

Data Flow – GK to SAP. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .13

Data Flow – SAP to GK. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .14

Explanation – Exchange Formats. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .15

Explanation of the Intermediate Documents (IDocs) Used. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15

Explanation of the SAP XI Web Services Used. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16

Explanation of the Cloud Function Module Generated Web Services Used. . . . . . . . . . . . . . . . . . . . . 17

Explanation of the Provided Integration Flows. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18

Integration Flow "GK POSLog to CAR". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18

Overview. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18

Description. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18

Responsible Identifiers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19

6.2

Integration Flow "GK POSLog XSLT Mapping". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19

Overview. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19

Description. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19

Responsible Identifiers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19

6.3

Integration Flow "Idocs-from-GK-to-SAP". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20

Overview. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20

Description. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20

Responsible Identifiers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .20

6.4

Integration Flow "Idocs-from-SAP-to-GK". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21

Overview. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21

Description. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21

2

PUBLIC

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Content

Responsible Identifiers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21

6.5

Integration Flow "SOAP-from-GK-to-SAP-RFC-WebServices". . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22

Overview. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .22

Description. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22

Responsible Identifiers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22

6.6

Integration Flow "SOAP-from-GK-to-SAP-XI-WebServices". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23

Overview. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .23

Description. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23

Responsible Identifiers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23

6.7

Integration Flow "SOAP-from-SAP-to-GK-
ProductMerchandiseViewReplicationBulkRequest_Out_Async_to_Sync". . . . . . . . . . . . . . . . . . . . . 24

Overview. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .24

Description. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24

Responsible Identifiers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Content

PUBLIC

3

1  Overview

SAP Cloud Integration (CI) is an application that acts as a middleman to establish a connection between
customer-specific applications, such as GK Software's applications, and SAP S/4HANA. In order for SAP CI to
work correctly with GK Software's applications, a configuration must first be performed by the customer, which
pre-made Integration Packages can assist with. The Integration Package from GK Software is described in this
documentation.

4

PUBLIC

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Overview

2

Installation

To install the GK Software Integration Package, click on the Discover icon in the top left corner of your CI
(represented by a compass symbol). You can then search for the term "GK Software Integration Package" and
the GK Software Integration Package will appear. Click on it and open it. In the Artifacts tab, you can now select
any artifact you want to install by simply clicking the Actions button. The installation of the artifact will start.

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Installation

PUBLIC

5

3  Configuration

3.1

First Step – Value Mapping in "Mapping LOGSYS to
Target"

In order for the GK Software Integration Package to work in the individual customer environment, some one-off
configurations must be made first. After importing the ZIP archive, you will notice that in addition to the
artifacts with the type Integration Flow, there are also two artifacts that are of the type Value Mapping. Scroll to
the artifact named Mapping LOGSYS to Target and open the artifact with one click.

The following table appears:

Now navigate to each line to make changes to the configuration. To do this, click on a row within the table. In
the lower part of the screen, the corresponding value mapping will open depending on the row. The following
screenshot shows, for example, the line for the identifier logsysws:

Adjust the URLs in the right-hand column according to your software environment. These are destination
addresses to which the transferred value from SAP CI can be sent afterwards. Make sure that all relevant URLs
are specified correctly as otherwise your software environment will not function correctly.

6

PUBLIC

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Configuration

3.2  Second Step – Endpoint Configuration for

the Integration Flow "SOAP-from-GK-to-SAP-XI-
WebServices"

The endpoints of the Integration Flows usually do not need to be adjusted by you. You can recognize these

endpoints by the dollar sign ($) followed by curly brackets ({}). These values are not adjusted and can be left
as the default values.

However, you must fill in the two Communication Component fields in the Processing tab in the SOAP-from-GK-
to-SAP-XI-WebServices Integration Flow.

Example

Endpoint address where the GK POS posts the outgoing message: "https://host:port/sap/xi/engine?
type=receiver&sap-client=100". You can also enter, for example, ${property.binding_url} to
dynamically read the value from a header or a property.

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Configuration

PUBLIC

7

3.3  Third Step – Configure the RFC Destination

To send IDocs from the SAP system to the GK Universal Connector (UCON), the RFC (Remote Function Call)
destination must first be defined once. Read below how this is possible with basic authentication:

Tab: Technical Settings

1. Log on to the central instance host of your SAP Customer Activity Repository (CAR).

2. Call transaction SM59.

3. Choose Create or select an existing SAP Forms service connection to change it.

4.

In the Technical Settings tab, enter at least the following:
• RFC destination: <SID>_CPI
• Connection type: G
• Description: HTTP Connection to External Server

5. Select Enter.

6. Select the Technical Settings tab and enter at least the following:

• <Target Host>

The host name is a combination of the subaccount name and your subaccount's technical name

<yoursubaccount:technicalname>.<yourregionhost:[xxx].hana.ondemand.com>
e.g.: namcfdev.it-cpi001-rt.cfapps.eu10.hana.ondemand.com

• Enter 443, which is the default SSL port of the SAP BTP service.
• <Path Prefix>

Enter the string: /SAP_OMNICHANNEL_POINT-OF-SALE_BY_GK/Idocs-from-SAP-to-GK

• Also specify the HTTP proxy parameters if an HTTP proxy is required for your ABAP system to access

the internet.

➜ Tab: Logon and Security

1. Select the Logon/Security tab and select Basic Authentication.

2.

3.

In the <User> and <Password> fields, enter the same user as is used in your subaccount (P-User), and the
password (please keep in mind possible future password changes).

In Security Options, select Active to enable SSL and specify the name of the SSL certificate store where
you imported the SAP BTP root certificate.

4. Save your entries.

 Note

If you perform the connection test in SM59, you get an HTTP 500 error. You can ignore this error message.

8

PUBLIC

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Configuration

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Configuration

PUBLIC

9

3.4  Optional – How do I know which identifier in the value
mapping matches my desired Integration Flow?

If you want to find out which identifier in the Value Mapping table belongs to which Integration Flow, this can be
seen from the respective Integration Flow. Open an Integration Flow, e.g. GK POSLog to CAR with one click. A
diagram opens, as shown in the following screenshot:

Follow the step-by-step instructions above by first opening the desired script (step 1). You can recognize the
scripts by a small scroll icon. Then drag the Apache Groovy script window upwards (step 2) so that you have
access to the Processing button (step 3). Now open the script file by clicking on the script file (step 4). The
Groovy script is then displayed and the identifier can be read. In this example, lines 12, 13, and 14 contain the
relevant information:

10

PUBLIC

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Configuration

3.5  Special Integration Flow "GK POSLog XSLT Mapping"

The Integration Flow GK POSLog XSLT Mapping has a special feature that allows you to extend the Integration
Flow individually with your requirements:

The file GKPOSLOG_Mapping.xsl is supplied in the Integration Package.

1. Copy the GK POS XSLT Mapping flow into your own Development Package

2. Change the XSLT

3. Configure the new process direct endpoint in the main flow.

3.6  Optional – How to find the correct URLs for an

Integration Flow configuration?

To find the correct URLs for configuring an Integration Flow, follow the step-by-step instructions below. This
is the GK POSLog to CAR Integration Flow, but for all other Integration Flows the same procedure must be
followed.

• Open the Integration Flow you want to configure and click Deploy (1). Then, make sure that the Integration

Flow is working correctly by checking that "Started" is displayed after "Runtime Status:" (2).

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Configuration

PUBLIC

11

• Now click on the eye icon (1) and then on the first box on the far left in the "Manage Integration Content"

section (2).

• Search for the relevant Integration Flow whose URL you want to find out (1) and then select it from the list
of search results (2). You can see the URL at the top of the detailed view of the Integration Flow. Click on
the clipboard icon to copy the URL to the clipboard for further use (3).

12

PUBLIC

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Configuration

4  Explanation – Data Flow Diagrams

4.1  Data Flow – GK to SAP

 Note

This graphic only shows an example of how the Integration Package works. The identifiers (logsys) in the
value mapping always allow multiple clients to be addressed. In the area marked by a red dotted line, 3
clients are used as an example and it shows that it is also possible to use several clients.

The area marked by a blue dotted line shows the different IDocs, which are transmitted here depending on
the CI.

1. Customer create

2. Customer change

3. Bill document read

4. Sales document read

The area marked by a green dotted line shows the different SAP XI Web Services, which are transmitted
here depending on the CI.

1. AssortmentERPRequestConfirmation_In

2. CustomerERPAddressBasicDataByNameAndAddressQueryResponse_In

3. CustomerERPByIDQueryResponse_In

4.

5.

InventoryByLocationAndMaterialQueryResponse_In

InventoryERPUnrestrictedStockByElementsQueryResponse_In

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
