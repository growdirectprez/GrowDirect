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

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Explanation – Data Flow Diagrams

PUBLIC

13

6. SalesOrderERPBasicDataByElementsQueryResponse_In

7. SalesOrderERPByIDQueryResponse_In_V3

8. SalesOrderERPChangeRequestConfirmation_In

9. SalesOrderERPCreateCheckQueryResponse_In

10. SalesOrderERPCreateRequestConfirmation_In_V2

4.2  Data Flow – SAP to GK

14

PUBLIC

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Explanation – Data Flow Diagrams

5  Explanation – Exchange Formats

5.1  Explanation of the Intermediate Documents (IDocs)

Used

The following IDocs are used for communication between GK Software and SAP ERP, SAP S/4 HANA or SAP
CAR.

IDoc Name

ADRMAS.ADRMAS03

CREMAS.CREMAS05

DEBMAS.DEBMAS07

DESADV.DELVRY07

ORDERS.ORDERS05

PROACT.PROACT01

REOPEX.REOPEX01

WBBDLD.WBBDLD05

WBBDLD.ZSORTLST_WBBDLD05

WPDCUR.WPDCUR01

WPDTAX.WPDTAX01

WPDWGR.WPDWGR01

WVINVE.WVINVE03

/ROP/BASE_PRICE./ROP/BASE_PRICE01

/ROP/PROMOTION./ROP/PROMOTION01

/ROP/PROMOTION./ROP/PROMOTION02

ORDCHG.ORDERS05

WBBDLD_TRIGGER01

Description

Address information

Vendor master data

Store and customer master data

Delivery notes

Orders created

Stock and sales data

Order proposals and exceptions

Item master data generated for the context of a specific
store

Item data; extended WBBDLD by additional layout data and
control point groups

Exchange rates

Tax rates

Material groups

Perpetual stock taking

Regular prices

OPP promotions

OPP promotions

Order changes

Trigger-IDoc HPR assortment list

The following IDocs are used for communication between SAP ERP, SAP S/4 HANA or SAP CAR and GK
Software.

IDoc Name

PORDCR1.PORDCR103

Description

Manually created orders (not SAP F&R)

Purchase order, stock transfer

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Explanation – Exchange Formats

PUBLIC

15

STATUS.SYSTAT01

WPUWBW.WPUWBW01

WVINVE.WVINVE03

RPO_DATA_TRANSFER01

*Returns status of IDoc

Goods receipt document

Perpetual stock taking

Purchase Order export

5.2  Explanation of the SAP XI Web Services Used

The required SAP XI Web Services used by the GK Central system and GK POS are exposed on the cloud.

SAP XI Web Service name

Description

AssortmentERPRequestConfirmation_In

Web service creates a new assortment and a layout module

CustomerERPAddressBasicDataByNameAndAddressQu
eryResponse_In

Web service allows customers to be searched

CustomerERPByIDQueryResponse_In

Web service is called using the following parameter: cus­

InventoryByLocationAndMaterialQueryResponse_I
n

InventoryERPUnrestrictedStockByElementsQueryR
esponse_In

tomer ID

Response: address details, communication details (tele­

phone, email, etc.)

Web service provides the current stock of an item

Web service returns items with negative stock

SalesOrderERPBasicDataByElementsQueryResponse
_In

Web service connects the POS Client to the customer order
management system in SAP ERP

SalesOrderERPByIDQueryResponse_In_V3

SalesOrderERPChangeRequestConfirmation_In

SalesOrderERPCreateCheckQueryResponse_In

SalesOrderERPCreateRequestConfirmation_In_V2

SalesPriceSpecCalcERPCreateRequestConfirmatio
n_In

StoreLayoutElementERPRequestConfirmation_In

Web service returns details of a customer sales order in SAP
ERP (a so-called "SD sales order"). It is called with the sales
order ID.

Web service is used to retrieve an existing customer sales
order in SAP ERP (a so-called "SD sales order"). The sales
order can be displayed or cancelled.

Web service allows a customer sales order to be simulated in
SAP ERP (a so-called "SD sales order").

Web service creates a customer sales order in SAP ERP (a
so-called "SD sales order"). It returns the customer sales
order ID.

Web service allows sales prices to be changed.

Web service changes an existing assignment of an item to a
shelf.

16

PUBLIC

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Explanation – Exchange Formats

TradeReceivablesPayablesAccountERPSplitItemGr
oupByCustomerIDQueryResponse_In

Web service is used for customer account balancing. It gives
the current status of a customer account, i.e. the (positive or
negative) open amount.

MerchandiseERPByElementsQueryResponse_In

Web service provides the details of an item; input=GTIN.

5.3  Explanation of the Cloud Function Module Generated

Web Services Used

Web services generated from function module are exposed on the cloud.

Cloud Function Module Generated Web Services name

Description

ZSSB_RFC_BILL_DOC_READ

ZSSO_RFC_SALES_DOC_READ

ZWS_BAPI_CUSTOMER_CHANGE

ZWS_BAPI_CUSTOMER_CREATE

Web service returns details of an invoice document

Web service returns details of a customer sales order

Web service for maintenance of existing SAP customers

Web service for creation of SAP customers

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Explanation – Exchange Formats

PUBLIC

17

6  Explanation of the Provided Integration

Flows

The following section provides an overview of all Integration Flow artifacts shipped with the GK Software
Integration Package. In addition to an overview graphic, you will also find a description of the artifacts, as well
as the respective identifiers, in order to make adjustments in the value mapping.

6.1

Integration Flow "GK POSLog to CAR"

6.1.1  Overview

6.1.2  Description

The task of the Integration Flow is to transport the data from GK POSLog to the SAP Customer Activity
Repository (CAR). It is possible to address different SAP CAR instances individually.

Another function is the possibility to call the Integration Flow GK POSLog XSLT Mapping [page 19], which
gives you the possibility to extend the Integration Flow by yourself.

18

PUBLIC

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Explanation of the Provided Integration Flows

6.1.3  Responsible Identifiers

• 'GK', 'logsys', input , 'CAR', 'car_binding_url'
• 'GK', 'logsys', input , 'CAR', 'car_credentials_id'
• 'GK', 'logsys', input , 'CAR' , 'cloud_connector_id'

6.2

Integration Flow "GK POSLog XSLT Mapping"

6.2.1  Overview

6.2.2  Description

The Integration Flow GK POSLog XSLT Mapping is not an independent Integration Flow, but must be
understood as a supplement to the Integration Flow GK POSLog to CAR [page 18]. It enables you to write
extension scripts for your workflows on your own.

6.2.3  Responsible Identifiers

Not applicable.

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Explanation of the Provided Integration Flows

PUBLIC

19

6.3

Integration Flow "Idocs-from-GK-to-SAP"

6.3.1  Overview

6.3.2  Description

The Integration Flow Idocs-from-GK-to-SAP transports data from the GK Universal Connector (UCON) to the
SAP system. As a target, it is possible to distinguish exactly which system is addressed within SAP (SAP CAR or
SAP S/4HANA), and it is also possible to address specific clients within the SAP system.

If you want to go the opposite way, you can use the Integration Flow Idocs-from-SAP-to-GK [page 21].

6.3.3  Responsible Identifiers

• 'GK', 'rcvprn_logsys', input , 'SAP', 'sap_binding_url_idoc'
• 'GK', 'rcvprn_logsys', input , 'SAP', 'sap_credential_id_idoc'
• 'GK', 'rcvprn_logsys', input , 'SAP' , 'sap_cloud_connector_id'

20

PUBLIC

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Explanation of the Provided Integration Flows

6.4

Integration Flow "Idocs-from-SAP-to-GK"

6.4.1  Overview

6.4.2  Description

The Integration Flow Idocs-from-SAP-to-GK transports data from the SAP system to the GK Universal
Connector (UCON). As a target, it is possible to distinguish exactly which UCON is addressed within GK, and it
is also possible to address specific clients.

If you want to go the opposite way, you can use the Integration Flow Idocs-from-GK-to-SAP [page 20].

6.4.3  Responsible Identifiers

• 'SAP', 'sender_logsys', input , 'GK', 'binding_url_idoc'
• 'SAP', 'sender_logsys', input , 'GK', 'credentials_id_idoc'

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Explanation of the Provided Integration Flows

PUBLIC

21

6.5

Integration Flow "SOAP-from-GK-to-SAP-RFC-
WebServices"

6.5.1  Overview

6.5.2  Description

This Integration Flow calls a desired SAP Remote Function Call (RFC) web service with GK data. The target is
automatically recognized and addressed accordingly.

6.5.3  Responsible Identifiers

• 'GK', 'logsysws', input , 'SAP', 'sap_binding_url_ws'
• 'GK', 'logsysws', input , 'SAP', 'sap_credentials_id_ws'
• 'GK', 'logsysws', input , 'SAP' , 'sap_cloud_connector_id_ws'

22

PUBLIC

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Explanation of the Provided Integration Flows

6.6

Integration Flow "SOAP-from-GK-to-SAP-XI-
WebServices"

6.6.1  Overview

6.6.2  Description

This Integration Flow calls a desired SAP NetWeaver Exchange Infrastructure (SAP XI) web service with GK
data. The target is automatically recognized and addressed accordingly.

This Integration Flow requires additional configuration once, as described in the Second Step – Endpoint
Configuration for the Integration Flow "SOAP-from-GK-to-SAP-XI-WebServices" chapter.

6.6.3  Responsible Identifiers

• 'GK', 'logsys', logsys , 'SAP', 'sap_binding_url_ws_xi'
• 'GK', 'logsys', logsys , 'SAP', 'sap_credentials_id_ws_xi'
• 'GK', 'logsys', logsys , 'SAP' , 'sap_cloud_connector_id_xi'
• 'SAP', 'ServiceName', interfacename , 'SAP' , 'ServiceNamespace'

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Explanation of the Provided Integration Flows

PUBLIC

23

6.7

Integration Flow "SOAP-from-SAP-to-GK-
ProductMerchandiseViewReplicationBulkRequest_Out_
Async_to_Sync"

6.7.1  Overview

6.7.2  Description

This Integration Flow uses SOAP (Simple Object Access Protocol) to transport Item Master Data from the SAP
system to the GK Universal Connector (UCON).

6.7.3  Responsible Identifiers

• 'SAP', 'Bussys', input , 'GK', 'ws_binding_url'
• 'SAP', 'Bussys', input , 'GK', 'ws_credentials_id'

24

PUBLIC

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Explanation of the Provided Integration Flows

Important Disclaimers and Legal Information

Hyperlinks

Some links are classified by an icon and/or a mouseover text. These links provide additional information.

About the icons:
• Links with the icon

: You are entering a Web site that is not hosted by SAP. By using such links, you agree (unless expressly stated otherwise in your

agreements with SAP) to this:
• The content of the linked-to site is not SAP documentation. You may not infer any product claims against SAP based on this information.
• SAP does not agree or disagree with the content on the linked-to site, nor does SAP warrant the availability and correctness. SAP shall not be liable for any

damages caused by the use of such content unless damages have been caused by SAP's gross negligence or willful misconduct.

• Links with the icon

: You are leaving the documentation for that particular SAP product or service and are entering an SAP-hosted Web site. By using

such links, you agree that (unless expressly stated otherwise in your agreements with SAP) you may not infer any product claims against SAP based on this

information.

Videos Hosted on External Platforms

Some videos may point to third-party video hosting platforms. SAP cannot guarantee the future availability of videos stored on these platforms. Furthermore, any
advertisements or other content hosted on these platforms (for example, suggested videos or by navigating to other videos hosted on the same site), are not within
the control or responsibility of SAP.

Beta and Other Experimental Features

Experimental features are not part of the officially delivered scope that SAP guarantees for future releases. This means that experimental features may be changed by

SAP at any time for any reason without notice. Experimental features are not for productive use. You may not demonstrate, test, examine, evaluate or otherwise use

the experimental features in a live operating environment or with data that has not been sufficiently backed up.

The purpose of experimental features is to get feedback early on, allowing customers and partners to influence the future product accordingly. By providing your

feedback (e.g. in the SAP Community), you accept that intellectual property rights of the contributions or derivative works shall remain the exclusive property of SAP.

Example Code

Any software coding and/or code snippets are examples. They are not for productive use. The example code is only intended to better explain and visualize the syntax
and phrasing rules. SAP does not warrant the correctness and completeness of the example code. SAP shall not be liable for errors or damages caused by the use of
example code unless damages have been caused by SAP's gross negligence or willful misconduct.

Bias-Free Language

SAP supports a culture of diversity and inclusion. Whenever possible, we use unbiased language in our documentation to refer to people of all cultures, ethnicities,
genders, and abilities.

SAP Omnichannel Point-of-Sale by GK, integration with SAP Customer Activity Repository,
SAP S/4HANA and SAP S/4HANA Cloud
Important Disclaimers and Legal Information

PUBLIC

25

www.sap.com/contactsap

© 2023 SAP SE or an SAP affiliate company. All rights reserved.

No part of this publication may be reproduced or transmitted in any form
or for any purpose without the express permission of SAP SE or an SAP
affiliate company. The information contained herein may be changed
without prior notice.

Some software products marketed by SAP SE and its distributors
contain proprietary software components of other software vendors.
National product specifications may vary.

These materials are provided by SAP SE or an SAP affiliate company for
informational purposes only, without representation or warranty of any
kind, and SAP or its affiliated companies shall not be liable for errors or
omissions with respect to the materials. The only warranties for SAP or
SAP affiliate company products and services are those that are set forth
in the express warranty statements accompanying such products and
services, if any. Nothing herein should be construed as constituting an
additional warranty.

SAP and other SAP products and services mentioned herein as well as
their respective logos are trademarks or registered trademarks of SAP
SE (or an SAP affiliate company) in Germany and other countries. All
other product and service names mentioned are the trademarks of their
respective companies.

Please see https://www.sap.com/about/legal/trademark.html for
additional trademark information and notices.

THE BEST RUN

