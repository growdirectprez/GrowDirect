GK/Retail SDK Omnichannel – App Enablement 2.0

GK/Retail OmniPOS

App Enablement 2.0

Version: 5.16.0

Copyright

© GK Software Group 2020. All rights reserved.

These materials are provided by GK Software SE and/or its affiliated companies (GK Software Group) for
informational purposes only without representation or warranty of any kind, and GK Software Group shall not be
liable for errors or omissions with respect to the materials.

The only warranties provided by GK Software Group are those that are set forth in the express warranty statements
in the individual agreements between GK Software Group and its Clients or Partners.  Nothing herein should be
construed as constituting an additional warranty.

No part of these materials shall be reproduced or transmitted to third parties in any form or for any purpose without
the express permission of GK Software Group. The information contained herein may be changed without prior
notice.

All company names of GK Software Group, GK Software Group’s product/services names as well GK Software
Groups logos mentioned herein are registered trademarks and intellectual property of GK Software Group.

App Enablement 2.0

III

Table of contents

1.4

1.3

1.4.1

1.3.1

1	 App Enablement API ..................................................................................................................................... 1
1.1	 Summary ...................................................................................................................................................... 1
1.2	 App Enablement API .................................................................................................................................... 1
1.2.1	 Architecture ........................................................................................................................................... 1
1.2.2	 Packages .............................................................................................................................................. 3
1.2.2.1	 File Common.js .............................................................................................................................. 3
1.2.2.2	 File  ExternalMasterdata.js ............................................................................................................. 4
1.2.2.3	 File Masterdata.js........................................................................................................................... 6
1.2.2.4	 File Pos.js ...................................................................................................................................... 7
1.2.3	 Supported Events ................................................................................................................................ 12
Implementation in POS Client (Full Client / Thin Client) ............................................................................... 12
Implementation details......................................................................................................................... 12
1.3.1.1	 GkAppApi interface ...................................................................................................................... 12
1.3.1.2	 AbstractGkAppApiImpl ................................................................................................................. 12
1.3.1.3	 JxBrowserGkAppApiV2Impl ......................................................................................................... 13
1.3.2	 Additional events supported by the POS Client (Full Client/Thin Client) ................................................ 14
1.3.2.1	 Hardware-related events and message prefixes ........................................................................... 14
1.3.2.2	 Flow events ................................................................................................................................. 14
1.3.3	 Project Extensibility ............................................................................................................................. 15
Implementation in Mobile Client UI5 ............................................................................................................ 16
Implementation details......................................................................................................................... 16
1.4.1.1	 posHostApi.js ............................................................................................................................... 16
1.4.1.2	 AppFactory.js ............................................................................................................................... 17
1.4.1.3	 DialogFactory.js ........................................................................................................................... 17
2	 Samples and Best Practises ....................................................................................................................... 17
2.1	 Example App .............................................................................................................................................. 17
2.2	 Register to barcode-scan event on the POS Client (Full Client/Thin Client) ................................................. 19
2.3	 Register Internal Line Item .......................................................................................................................... 20
2.3.1	 Minimal Request ................................................................................................................................. 20
2.3.2	 Extended Request ............................................................................................................................... 20
2.3.2.1	 Minimal Promotion Data ............................................................................................................... 20
2.3.2.2	 Maximal Promotion Data .............................................................................................................. 21
2.3.3	 Sales Order Pickup ............................................................................................................................. 23
2.4	 Register External Line Item ......................................................................................................................... 23
2.4.1	 Minimal Request ................................................................................................................................. 23
2.4.2	 Extended Request ............................................................................................................................... 24
2.4.2.1	 Minimal Promotion Data ............................................................................................................... 24
2.4.2.2	 Maximal Promotion Data .............................................................................................................. 27
2.4.3	 Pay-in Line Item .................................................................................................................................. 30
2.4.4	 Pay-out Line Item ................................................................................................................................ 30
2.4.5	 Sales Order Pickup ............................................................................................................................. 31
2.4.6	 Down Payment Clearing ...................................................................................................................... 31
2.5	 Cancel Current Transaction ........................................................................................................................ 31
2.5.1	 Minimal Request ................................................................................................................................. 31
2.5.2	 Maximal Request ................................................................................................................................ 31
2.6	 Register Customer ...................................................................................................................................... 32
2.6.1	 Minimal Request ................................................................................................................................. 32
2.6.2	 Maximal Request ................................................................................................................................ 32
2.7	 Create Transaction Extension ..................................................................................................................... 32
2.8	 Update Transaction Extension .................................................................................................................... 32
2.9	 Delete Transaction Extension ..................................................................................................................... 32
2.10	 Add Printout Data ....................................................................................................................................... 33
2.10.1	 Register Internal Line Item with Additional Printout Data ...................................................................... 33
2.10.2	 Register External Line Item with Additional Printout Data ..................................................................... 33
2.10.3	 Add Additional Transaction Report ...................................................................................................... 33

IV

App Enablement 2.0

App Enablement 2.0

1

1  App Enablement API

1.1  Summary

The term app-enabled describes the ability to add custom functionality to a client application like, for example, a
POS Client by using apps and by allowing the interaction between such an app and the supporting client
application.

Such an app can call backbone services in the enterprise or may provide its own business logic in its own backend.
It may react to events generated by the client and call functions provided by the App Enablement API to make the
supporting client react to an action or an event in the app.

The interaction between an app and the supporting client is based on listener mechanisms and events:

•  The communication from client to app is realized by a listener concept:

To allow the app to react to events in the client, listeners can be registered (method registerListener, see
below).
As a result, an app can, for example, react to a scan event or to the registration of an item by showing item
details or recommendations that are called by the app from a respective backend system.

•  The communication from app to client is realized by a set of JavaScript API functions:

The App Enablement API provides a set of methods that can be called to make the supporting client react to
the events or actions in the app or actively ask the client for more information.
As a result, the system can for example take an item that has been searched and found in the app and
register it to the transaction in the client.

An example of application using App Enablement could be a recommendation application running in the POS. This
application might be hooked on the registration process and recommend additional, better, or cheaper products
based on currently registered items. Such applications could be created by a partner company and loaded from a
remote server.

This document has three chapters: The first chapter describes the general API that is provided for apps, the
second chapter illustrates the respective implementation in the POS Client (Full Client/Thin Client), and the third
chapter describes the implementation in the Omnichannel Point-of-Sale Mobile Client UI5.

1.2  App Enablement API

The functionality is provided for a JavaScript application running in the host application.

GK/Retail Omnichannel Point-of-Sale of version 5.5 supports a new version of the App Enablement API that is
consistent in structure, terminology, and functionality. The new version of the API provides different JavaScript
files, each focusing on a certain functionality and bundling functions that are relevant for a certain group of clients.

So, for example, for a POS Client, all JavaScript files of the API may be implemented while for other clients only
one or selected files are relevant.

1.2.1 Architecture

A JavaScript application is hosted in a host application (POS Full or Thin Client, Mobile Client UI5) that serves as
container. App Enablement provides functionality of the host application for the JavaScript application running in it.

The JavaScript application contains a client part of App Enablement - connector and APIs. The connector
establishes communication between APIs and the host, APIs provide the functionality bundled for different
purposes and client groups.

2

App Enablement 2.0

It differs how the JavaScript application is running in the host application:

The POS Client (full and thin) is a desktop Java application featuring an embedded browser that is used to run the
JavaScript application.

The Mobile Client UI5 runs in a browser on a mobile device. The JavaScript application is loaded in an IFrame.

If the JavaScript application is running in an embedded browser, the Connector calls an URL in order to invoke a
functionality in the host application. The URL contains a special protocol name jmc. There is a protocol handler
registered for this special protocol in the embedded browser (on server side). The handler parses the request and
calls the API.

If the JavaScript application is running in an IFrame, the Connector uses a window.postMessage() in order to
invoke a functionality in the host application. This method comes from HTML5 and allows sending messages
between windows/frames across domains.

App Enablement 2.0

3

1.2.2 Packages

1.2.2.1 File Common.js

Description

The file provides basic App Enablement functionality, that is, general functions that are relevant for all kinds of
clients.

Namespace

comGkSoftwareGkrAppEnablementApi.Common

Supported methods

Method
oAppEnablement

Parameters
sResultFunction,
sErrorFunction

CommonInstance.

getSessionContext

Description
Calls for context information
on the current user session
of the hosting client, like, for
example, the user language
or the tenant or store ID to
which the user is logged in.

Example

•  Get the user's language to display texts in the

respective language.

•  Get tenant and store to display store-specific

content.

Since
2.0.0

Example response object:

{
  businessUnitGroupID:
"100000000000000001",
  businessUnitID: "9090", // Equivalent
to store ID
  isoCurrencyCode: "USD",
  storeLanguage: "en_US",
  tenantID: "004",
  userLanguage: "zh_CN",
  workstationID: "107"
}

Example request object:

2.0.0

Creates a request object for
the function
registerListener.
The function will also
"stringify" the complete object
for the passed parameters.

oAppEnablement

CommonInstance.

sEventName,
sEventListenerName,

bPassData

createRegister

ListenerRequest

4

App Enablement 2.0

Method

Parameters

Description

Example

Since

oAppEnablement

sRegisterListenerRequest

CommonInstance.

registerListener

oAppEnablement

          sEventName,
sEventListenerName

CommonInstance.

createUnregister

ListenerRequest

oAppEnablement

sEvent

CommonInstance.

unregisterListener
oAppEnablement

CommonInstance.

closeBrowser
oAppEnablement

CommonInstance.

hideBrowser
oAppEnablement

sResultFunction,
sErrorFunction

CommonInstance.

getOperatorData

{
  "event": "EVENT_TRANSACTION_UPDATED",
  "listener":
"returnEventNotification",
  "passData": false || true
}

Allow the app to react for example to a hardware-
related event like the opening of the cash drawer or to
an error event like an error during printing.

2.0.0

Example request object:

2.0.0

{
  itemID: "030039",
  language: "en_US",
  isoCurrencyCode: "USD"
}

Registers a listener for the
given event so that the app
can react to that event. If
passData in the request
object is set to true, the
function hands back the
notification and the complete
event including the event
message.
Creates a request object for
the function
unregisterListener.
The function will also
"stringify" the complete object
for the passed parameters.

Removes the listener for the
given event.

Unregister the listeners so that the app can log off the
event bus.

2.0.0

Closes the App and disposes
of browser instance.

Hides the App without
closing it (keeps browser
state).

Calls for information on the
current operator, like, for
example, the operatorID, the
name of the operator and the
operators current rights.

2.1.0

2.1.0

2.1.0

Example response object:

{
  operatorID: "1",
  workerID: "1",
  salutation: "Mr.",
  firstName: "John",
  lastName: "Doe",
  rightsSet:
["S.00000000001.00","S.00000000001.01"]
}

1.2.2.2 File  ExternalMasterdata.js

Description

The file provides functions that deal with master data that is accessible from an external repository.

App Enablement 2.0

Namespace

comGkSoftwareGkrAppEnablementApi.ExternalMasterdata

Supported methods

5

Method
oAppEnablement

ExternalMasterdata

Instance.createGet

ItemByCriteria

Request
oAppEnablement

Parameters
sItemID,
oContext

Description
Creates a request object for function
getItemByCriteria. The function will also
"stringify" the complete object for the passed
parameters.

Example
Example request object:

Since
2.0.0

{
  "event":
"EVENT_TRANSACTION_UPDATED",
  "listener":
"returnEventNotification"
}

sResultFunction,

Calls and hands back details of an item from an
external repository.

Call details of an item that is available in
a connected web shop.

2.0.0

ExternalMasterdata

sErrorFunction,

Instance.get

          oGetItemBy

ItemByCriteria

oAppEnablement

ExternalMasterdata

Instance.createGet

ItemListBySearch

CriteriaRequest
oAppEnablement

CriteriaRequest
sSearchQuery,
oContext

Creates a request object for function
getItemListBySearchCriteria. The
function will also "stringify" the complete object
for the passed parameters.

Example request object:

2.0.0

{
  query: "camera",
  language: "en_US",
  isoCurrencyCode: "USD",
  recordCount: 60
}

sResultFunction,

Calls and hands back a list of items from an
external repository.

Search for items in a connected web
shop, display a list of results.

2.0.0

ExternalMasterdata

sErrorFunction,

Instance.getItem

          oGetItemList

ListBySearch

Criteria

oAppEnablement

ExternalMasterdata

Instance.createGet

ExternalImage

UrlRequest
oAppEnablement

BySearchCriteria

          Request
sItemID,
oContext

Creates a request object for the function
getImageUrl. The function will also "stringify"
the complete object for the passed parameters.

 Example request object:

2.0.0

{
  itemID: "030039",
  type: "item",
  language: "en_US",
  isoCurrencyCode: "USD"
}

sResultFunction,

Provides an image URL for external items.

2.0.0

ExternalMasterdata

sErrorFunction,

Instance.getImageUrl

oGetExternal

6

Method

Parameters
ImageUrlRequest

Description

Example

Since

App Enablement 2.0

1.2.2.3 File Masterdata.js

Description

The file provides functions that deal with internal master data like, for example, item details for items that are
contained in the master data.

Namespace

comGkSoftwareGkrAppEnablementApi.Masterdata

Supported methods

Parameters

sItemID

Method

oAppEnablement
MasterdataInstance
.
createGetItem
DataByIDRequest

Description

Example

Creates a request object for function
getItemDataByID.

  Example request
object:

Sinc
e
2.0.0

The function will also "stringify" the
complete object for the passed
parameters.

{
  itemID:
"030039"
}

oAppEnablement
MasterdataInstance
.
getItemDataByID

sResultFunction,
sErrorFunction,
oGetItemInformationByIDRequest

Provides GK master data item
information for a given item ID.

oAppEnablement
MasterdataInstance
.
createGetItem
DataListByID
ListRequest

aItemIDList

Creates a request object for function
getItemDataListByIDList.

The function will also "stringify" the
complete object for the passed
parameters.

2.0.0

Make the client
open the
item information
screen for the given
item ID.

Show item details
for a selected item.
Thus, for example,
additional
information about a
recommended item
can be displayed.
Example request
object:

2.0.0

{

itemIDList
:
["03039",
"65005",
"65007"]
}

oAppEnablement

Masterdata

sResultFunction,
sErrorFunction,
oGetItemDataListByIDListReques
t

Returns list of items for the list of
given item ids
(Note that only existing items are
handed back; therefore, the return
index of the resulting items is not the
same than that of the IDs handed
in).

•  Display a list
of items.
•  Analyze list
and display
result of
analysis.

2.0.0

App Enablement 2.0

Method

Parameters

Description

Example

7

Sinc
e

Instance.

getItemDataListByIDList
oAppEnablement

sItemID

MasterdataInstance
.

createGetImage

UrlRequest

Creates a request object for function
getImageUrl.

Example request
object:

2.0.0

The function will also "stringify" the
complete object for the passed
parameters.

{
  itemID:
"03039",
  type:
"item"
}

oAppEnablement

MasterdataInstance.

sResultFunction,
sErrorFunction,
oGetImageUrlRequest

Returns the image URL for the given
item ID.

Use URL to call
and display item
images.

2.0.0

getImageUrl

1.2.2.4 File Pos.js

Description

The file provides functions that are specific for POS Clients, for example, dealing with POS transactions.

Namespace

comGkSoftwareGkrAppEnablementApi.Pos

Supported methods

Method

Parameters

Description

Example

Si
nc
e
2.
0.
0

Example request object:

{
  itemID:
"030039"
}

oAppEnablement

sItemID

PosInstance.

createGetPOS

ItemInformation

ByIDRequest

oAppEnablement

PosInstance.

getPOSItem

InformationByID

•  InformationByIDReques

t

•  oGetPOSItem
•  sErrorFunction
•  sResultFunction

Creates a request
object for function
getPOSItemIn
formationByI
D.

The function will
also "stringify" the
complete object for
the passed
parameters.
Returns
item information for
the given item ID.

Make the client open the
item information screen
for the given item ID.

2.
0.
0

Enriched with
additional POS-
specific information
provided by other

Show item details for a
selected item. Thus, for
example, additional
information about a

8

Method

oAppEnablement

PosInstance.

createRegister

LineItemRequest

oAppEnablement

PosInstance.

registerLineItem

App Enablement 2.0

Parameters

Description

Example

sItemID, oContext

services like, for
example, stock.
Creates a request
object for function
registerLine
Item.

The function will
also "stringify" the
complete object for
the passed
parameters.

recommended item can
be displayed.
Example request object:

{
  "itemID":
"030039",
  "language":
"en_US",

"isoCurrencyCode
": "USD"
}

Si
nc
e

2.
0.
0

•  oRegisterLineItemRequ

est

•  sErrorFunction
•  sResultFunction

oAppEnablement

Required attributes:

PosInstance.

createRegister

ExternalLine

ItemRequest

•  iQuantity
•  sActualUnitPrice
•  sItemID
•  sItemType
•  sMainPOSItemID
•  sPosItemID
•  sReceiptText
•  sRegistrationNumber
•  sTaxGroupID
•  sUnitOfMeasureCode

Optional attributes:

•  aLineItemExtensionLis

t

•  aPrintAdditionalLineI

temTextLineList

•  aRetailPriceModifierL

ist

•  aRetailTransactionLin
eItemI18NTextList
•  aSaleReturnLineItemCh

aracteristicList

•  aSaleReturnLineItemMe
rchandiseHierarchyGro
upList

•  bAllowFoodStampFlag
•  bDiscountFlag

Registers a
line item for the
given item ID.

Register an item and thus
add the item to the
transaction.

2.
0.
0

Creates a request
object for function
registerExte
rnalLineItem
.

The function will
also "stringify" the
complete object for
the passed
parameters.

Add items that are
displayed in the app (for
example, recommended
items) to the transaction.
Example request object
(minimal request, contains
all required attributes):

2.
0.
0

{

"posItemID":"363
6",

"itemID":"4711",

"unitOfMeasureCo
de":"PCE",

"itemType":"CO",

"actualUnitPrice
":15.55,
  "quantity":1,

"receiptText":"T
est Item",

"registrationNum
ber":"3636",

"mainPOSItemID":
"3636",

"taxGroupID":"A1
"
}

App Enablement 2.0

Method

Parameters

Description

Example

9

Si
nc
e

•  bFrequentShopperPoint

sEligibilityFlag

•  bNotConsideredByLoyal

tyEngineFlag

•  bProhibitReturnFlag
•  bProhibitTaxExemptFla

g

•  bWicFlag
•  oRetailTransactionLin
eItemAdditionalParame
terList

•  oSaleReturnLineItemSa

lesOrderObject
•  sDepositTypeCode
•  sDiscountTypeCode
•  sHeight
•  sItemClassCode
•  sLength
•  sMainMerchandiseHiera

rchyGroupID

•  sMainMerchandiseHiera
rchyGroupIDQualifier
•  sMerchandiseHierarchy

GroupDescription

•  sMerchandiseHierarchy

GroupName

•  sPosDepartmentID
•  sPriceChangeTypeCode
•  sPriceTypeCode
•  sQuantityInputMethod
•  sReasonCode
•  sReasonCodeGroupCode
•  sReasonDescription
•  sReceiptDescription
•  sRegularUnitPrice
•  sSerialNumber
•  sTareCount
•  sTaxExemptCode
•  sUnits
•  sWarrantyDuration
•  sWidth

•  LineItemRequest
•  oRegisterExternal
•  sErrorFunction
•  sResultFunction

Registers a line
item based on
external item data.

Register an item and thus
add the item to the
transaction.

2.
0.
0

Add items that are
displayed in the app (for
example, recommended
items) to the transaction.

sResultFunction,

sErrorFunction

Returns the current
transaction.

2.
0.
0

oAppEnablement

PosInstance.

registerExternal

LineItem
oAppEnablement

10

Method

PosInstance.

getCurrent

Transaction
oAppEnablement

PosInstance.

getCurrent

CustomerList

oAppEnablement

PosInstance.

createCancel

CurrentTransaction

Request
oAppEnablement

PosInstance.

cancelCurrent

Parameters

Description

Example

App Enablement 2.0

sResultFunction,

sErrorFunction

Returns all
customers that are
registered at the
current transaction.

sReasonCode,
sReasonDescription

Creates a request
object for function

sResultFunction, sErrorFunction, {}

•  Display customers.
•  Get list of

customers and use
that to call
additional
information about
these customers via
other (project-
specific) services.

{
  "reasonCode":
"abc",

"reasonDescripti
on": "A
cancellation."
}

{
  "customerId":
"10012"
}

cancelCurrent

Transaction.

Allows to cancel
the current
transaction in the
POS.

Creates a request
object for function

registerCustomer.

Allows to register a
customer within the
current transaction
in the POS.

Creates a request
object for function
addTransacti
onExtension.

{

"extensionKey":
"key",

"extensionValue"
: "val"
}

Si
nc
e

2.
0.
0

2.
1.
0

2.
0.
0

2.
0.
0

2.
0.
0

2.
0.
0

2.
0.
0

Transaction
oAppEnablementPosInstance.create
RegisterCustomerRequest

sCustomerId

oAppEnablement

PosInstance.

registerCustomer

sResultFunction,

sErrorFunction,

oRegister

CustomerRequest

 oAppEnablementPosInstance.creat
eAddTransactionExtensionRequest

 sExtensionKey,
sExtensionValue

oAppEnablement

PosInstance.

sResultFunction,
sErrorFunction,
oAddTransactionExtensionR
equest

Allows to add an
extension to the
current transaction
in the POS.

App Enablement 2.0

Method

Parameters

Description

Example

addTransaction

Extension
oAppEnablementPosInstance.create
UpdateTransactionExtensionReques
t

sExtensionKey,
sExtensionValue

oAppEnablementPosInstance.update
TransactionExtension

oAppEnablementPosInstance.create
DeleteTransactionExtensionReques
t

oAppEnablementPosInstance.delete
TransactionExtension

oAppEnablementPosInstance.create
AddAdditionalTransactionReportRe
quest

oAppEnablement

PosInstance.

addAdditional

          TransactionReport
oAppEnablement

PosInstance.

createEnter

CouponRequest

Creates a request
object for function
updateTransa
ctionExtensi
on.

Allows to update
an extension in the
current transaction
in the POS.

Creates a request
object for function
deleteTransa
ctionExtensi
on .

{

"extensionKey":
"key",

"extensionValue"
: "val"
}

{

"extensionKey":
"key"
}

sResultFunction,
sErrorFunction,
oUpdateTransactionExtensi
onRequest
sExtensionKey

sResultFunction,
sErrorFunction,
oDeleteTransactionExtensi
onRequest
sReportIdentification,

Allows to delete an
extension in the
current transaction
in the POS.

Creates a request
object for function

aPrintAdditional

addAdditional

LineItemTextLineList

TransactionReport.

sResultFunction,
sErrorFunction,
oAdditionalTransactionRep
ortRequest

Allows to add an
additional receipt
to the current
transaction in the
POS.

{

"reportIdentific
ation" :"",

"printAdditional
LineItemTextLine
List" : ["",""]
}

sCouponNumber, sPrivilegeType,
dPrivilegeValue

Creates a request
object for function

Example request object:

enterCoupon.

{

"couponNumber":
"1",

"privilegeType":
"RP",

"privilegeValue"
: "1"
}

oAppEnablement

PosInstance.

sResultFunction,

sErrorFunction,

Allows to enter a
coupon to the
current transaction
in the POS.

11

Si
nc
e

2.
0.
0

2.
0.
0

2.
0.
0

2.
0.
0

2.
0.
0

2.
0.
0

2.
1.
0

2.
1.
0

12

Method

App Enablement 2.0

Parameters

Description

Example

Si
nc
e

enterCoupon

oEnterCouponRequest

1.2.3 Supported Events

The App Enablement API allows the apps to register to standard events of the POS Client. For this purpose,
the  registerListener  method is provided. It expects two parameters: firstly, the name of an event sent by the
POS and secondly, the name of a JavaScript function to be called when this event occurs.

Each client has to implement the events that shall be reacted on by the apps. The following table shows the events
implemented for both POS Clients:

Description
Event fired when transaction is updated

Event name
EVENT_TRANSACTION_UPDATED

Note that this list will be iteratively enhanced in future releases.

1.3  Implementation in POS Client (Full Client / Thin Client)

1.3.1 Implementation details

The following sections describe the technical realization of the app-enabled feature in Omnichannel Point-of-Sale.

For embedding applications in form of HTML5 with JavaScript support, the embedded JxBrowser is used.
JxBrowser is based on the modern Chromium engine.

There are three basic interfaces that make up the structure for the app-enabled feature:

•  The GkAppComponent is the UI element that represents the app. This is nothing more than a simple Swing

component that hosts the intrinsic app.

•  The GkAppApi is the Java side representation of the API that is also exposed to the JavaScript side.
•  The GkAppApiFactory is a factory to produce GkAppApi instances on behalf of a GkAppComponent. All
these interfaces are an abstraction from the concrete technology, due to that there are usually abstract
implementations and JxBrowser-specific implementations.

•  The AppApiHandler are used to encapsulate the Java method implementation for all methods per

namespace.

1.3.1.1 GkAppApi interface

The GkAppApi is intended to encapsulate the API that is exposed to the app and also acts as a wrapper for the
app. The interface is quite thin - it allows calling a function in an asynchronous fashion and register and unregister
listeners. Since this interface is intended to be technology neutral, all input and output parameters are declared
here as strings.

1.3.1.2 AbstractGkAppApiImpl

The AbstractGkAppApiImpl is a convenience, abstract base implementation of this interface. It basically
implements just the listener management (besides invocation of listeners) and has an injected ServiceLocator
in order to access POS Services. In addition, this abstract class is technology neutral but provides some
infrastructure common to all other implementations.

Although this method has no implementation for the call method (and therefore no real strategy how to delegate the
method calls to real Java calls), it makes the basic assumption that each invocation of call will end up in a

App Enablement 2.0

13

corresponding method call of this class. Due to that, this class also contains concrete implementations of API
methods that are technology-neutral (such as getCurrentTransaction) but it provides no strategy how to call it -
this is the job of concrete subclasses.

1.3.1.3 JxBrowserGkAppApiV2Impl

The JxBrowserAppApiV2Impl is the implementation that is tied to the embedded browser technology.
Technically, this class is a wrapper for the Chromium Browser Engine that extends the AbstractGkAppApiImpl.
It basically uses two JxBrowser techniques to provide the implementation:

•  By implementing the interface DefaultNetworkDelegate and adding it to JxBrowser, it is possible to resolve
installation-specific paths (for example, the location of the JavaScript API that comes with the installation).
•  By implementing the interface ScriptContextListener, it is possible to decode JavaScript requests from the
app and call corresponding Java methods. The interface has been already implemented by JxBrowser’s
abstract class ScriptContextAdapter. There are two methods: onScriptContextCreated (which is invoked
when a JavaScript context has been created) and onScriptContextDestroyed (which is invoked when a
JavaScript context has been destroyed). With creating an anonymous class of ScriptContextAdapter, these
methods can be overwritten without the need of extending ScriptContextAdapter and the class can be
added as a listener to JxBrowser.

Implementation of protocol listeners

The JxBrowserAppApi registers some protocol listeners for the following protocols:

Protocol
posjs://
jmc://

Meaning
Protocol to import product/project specific JavaScript files, also used to encode function calls.
Protocol to encode Java method calls.

The protocol evaluation is done through the invocation of the implemented method
DefaultNetworkDelegate.onBeforeURLRequest , which decides what to do in each case. In case of pojs:// ,
some resources should be served (technically, it only overrides the URL to the specific static resource) and in case
of jmc:// , the call is translated to some Java method call.

Implementation of the ScriptContextListener.onScriptContextCreated

Function calls on JavaScript side are handled in this way: Consider you have a JavaScript method with the
following signature:

oAppEnablementCommonInstance.getSessionContext(resultFunction, errorFunction)

Semantics: Gets the session context information as described in the API. In case everything works as expected
and a session context can be created and returned, the method  resultFunction is called,
otherwise  errorFunction . The implementation of this method constructs a URL for the  jmc://  protocol. The
path part of the URL is the name of the namespace plus the Java method to be called (typically the same as the
Java method). The query part contains the parameters and the callbacks.

So you receive the following URL:

14

App Enablement 2.0

jmc://comGkSoftwareGkrAppEnablementApi.Common/getSessionContext?onResult=resultFunction&onError=errorFunction

This URL is passed to the injected browser function. In this method, the request is decoded (each input and output
parameter is interpreted as a JSON object) and the corresponding Java method is called. Upon completion of the
Java method, the  onError  or  onResult  callback is invoked.

1.3.2 Additional events supported by the POS Client (Full Client/Thin Client)

1.3.2.1 Hardware-related events and message prefixes

Description
Scanner data event
MSR data event
Cash drawer event - cash drawer opened
Cash drawer event - cash drawer closed
General printer error event
Printer event - offline
Printer event - hangup
Printer event - out of paper
Printer event - cover opened
Printer event - cover closed
Printer event - status OK
Print finished event
General terminal events
General terminal error event
Terminal event - signon started
Terminal event - signon finished
Terminal event - signoff started
Terminal event - signoff finished
Terminal event - payment started
Terminal event - payment finished

1.3.2.2 Flow events

Event name
EVENT_POS_INPUT_SCANNER_DATA
EVENT_POS_INPUT_MSR_DATA
EVENT_CASH_DRAWER_OPENED
EVENT_CASH_DRAWER_CLOSED
ERROR_EVENT_PRINTER
ERROR_EVENT_PRINTER_OFFLINE
ERROR_EVENT_PRINTER_HANGUP
ERROR_EVENT_PRINTER
ERROR_EVENT_PRINTER_COVER_OPENED
EVENT_PRINTER_COVER_CLOSED
EVENT_PRINTER_STATUS_OK
EVENT_PRINTER_PRINT_FINISHED
EVENT_TERMINAL
ERROR_EVENT_TERMINAL
EVENT_TERMINAL_SIGNON_STARTED
EVENT_TERMINAL_SIGNON_FINISHED
EVENT_TERMINAL_SIGNOFF_STARTED
EVENT_TERMINAL_SIGNOFF_FINISHED
EVENT_TERMINAL_PAYMENT_STARTED
EVENT_TERMINAL_PAYMENT_FINISHED

Event name
FLOW_EVENT_POS_STARTED

FLOW_EVENT_SIGNED_ON
FLOW_EVENT_SIGNED_OFF
FLOW_EVENT_POS_LOCKED
FLOW_EVENT_POS_UNLOCKED
FLOW_EVENT_INACTIVITY_TIMER

Description
Event fired when the POS is started (start of
the main flow)
Event fired when the POS is signed on
Event fired when the POS is signed off
Event fired when the POS is locked
Event fired when the POS is unlocked
Event fired when the inactivity timer timeout is
reached
Event fire when the POS entered
item registration main step
Event fired when the POS is in
registration mode without a transaction
Event fire when the POS entered payment
main step
Event fired when the POS is in payment mode
with grand total in base currency
Event fired when the POS is in payment mode
and the currency changed
Event fired when the POS is in change mode  FLOW_EVENT_CHANGE
Event fired when payment mode is canceled  FLOW_EVENT_PAYMENT_CANCELED

FLOW_EVENT_PAYMENT_GRANDTOTAL

FLOW_EVENT_PAYMENT_MAIN_ENTERED

FLOW_EVENT_REGISTRATION_MAIN_ENTERED

FLOW_EVENT_REGISTRATION_NO_TRANSACTION

FLOW_EVENT_PAYMENT_GRANDTOTAL_CURRENCYCHANGED

App Enablement 2.0

15

Event name
FLOW_EVENT_CUSTOMER_FLOW_PAYMENTEND_TRANSACTION_FINISHED_ENTERED

FLOW_EVENT_PAYMENTEND_SCO_TRANSACTION_FINISHED_ENTERED

EVENT_SALERETURNLINEITEM_UPDATED_SERIALNUMBER

FLOW_EVENT_CUSTOMER_FLOW_PAYMENTEND_TIMER

EVENT_TRANSACTION_RECOVERED
EVENT_SALERETURNLINEITEM_UPDATED_REGISTERED

EVENT_SALERETURNLINEITEM_UPDATED_QUANTITY

EVENT_SALERETURNLINEITEM_UPDATED_PRICE

FLOW_EVENT_PAYMENTEND_SCO_TIME

EVENT_TRANSACTION_PAYED
EVENT_TRANSACTION_CLOSED

Description
Event fire when the POS entered customer
flow payment end transaction finished step
Event fired when the customer flow timer
timeout is reached
Event fired when the PaymentEndSco flow
timer timeout starts
Event fired when the PaymentEndSco flow
timer timeout is reached
Event fired when transaction is payed
Event fired when transaction is finalized or
canceled
Event fired when transaction is recovered
Events fired when a sale return line item is
created
Event fired when a sale
return line item quantity is updated
Event fired when a sale return line item price
is updated
Event fired when a sale return line item serial
number is updated
Event fired when a sale return line item is
recovered
Events fired when a voids line item is created
or updated
Events fired when a voids line item is
recovered
Event fired when line item discount applied
Event fired when line item reduction applied  EVENT_LINEITEM_REDUCTION_APPLIED
Event fired when a line item was closed
Event fired when a total is created
Events fired when a tender line item was
voided
Events fired when a tender line item is created
or updated
Events fired when the currency changed and a
tender line item is updated
Event fired when transaction discount applied  EVENT_TRANSACTION_DISCOUNT_APPLIED
Event fired when transaction reduction applied  EVENT_TRANSACTION_REDUCTION_APPLIED
Event fired when a customer is registered
Event fired when POS switched to offline
mode
Event fired when POS switched to online
mode

EVENT_LINE_ITEM_CLOSED
EVENT_TOTAL_CREATED
EVENT_TENDERLINEITEM_VOIDED

EVENT_CUSTOMER_REGISTERED
POS_STATUS_OFFLINE_EVENT

EVENT_LINEITEM_DISCOUNT_APPLIED

POS_STATUS_ONLINE_EVENT

EVENT_VOIDSLINEITEM_UPDATED_REGISTERED

EVENT_VOIDSLINEITEM_UPDATED_RECOVERED

EVENT_TENDERLINEITEM_UPDATED_REGISTERED

EVENT_SALERETURNLINEITEM_UPDATED_RECOVERED

EVENT_TENDERLINEITEM_UPDATED_CURRENCYCHANGED

1.3.3 Project Extensibility

A project can implement new JavaScript methods with the backend Java methods and override Java backend
methods for already existing JavaScript methods of the App Enablement API.

•  Override Java backend methods
•

Implement the interface com.gk_software.pos.api.ui.component.app.AppApiExtension.
Implement the methods that shall be overridden.

•
•
•  Define responsible Namespaces for this extension class (handled via

•

AppApiExtension.isNamespaceHandler(...) method).
In your component-descriptor.xml, export the implementation (via component:export-bean) as a
bean with the mandatory name  appApiExtension and
interface com.gk_software.pos.api.ui.component.app.AppApiExtension.

16

•
•

Implement new JavaScript methods and Java backend

App Enablement 2.0

•  Create a new JavaScript file, for example,  api_ext.js. For inclusion of this new JavaScript file, there are

two possibilities:

1.  It can be bundled and included into apps like product API (standard way to include JavaScript files),

for example:

<script type="text/javascript" src="./libs/appEnablement/api/api_ext.js"></script>

2.  It can be bundled with the POS

1.  Add the file to deployment so that it is available at runtime in the POS_ROOT_DIR directory (for

example, POS_ROOT_DIR/x/y/api_ext.js ).

2.  Include the new JavaScript file to your application by using special protocol posjs:

<script src="posjs://x/y/posapi_ext.js">

Hence, JavaScript extensions can be placed everywhere under POS_ROOT_DIR, you only have to
guarantee that the same path is used in the script tag in HTML files.

•

Implement the corresponding Java backend methods. The steps are the same as in point "Override Java
backend methods".

1.4  Implementation in Mobile Client UI5

1.4.1 Implementation details

The following sections describe how to implement App Enablement apps in the Mobile Client UI5 with HTML5
(JavaScript / UI5). The technology that is used to display App Enablement apps is a normal HTML IFrame.

There are three major entry points in the Mobile Client to realize App Enablement. Therefore, we will have a
look on the important parts and packages of the source code:

•  Omnichannel POS/libs/posHostApi.js
•  Omnichannel POS/appEnablement

factory/AppFactory.js

•
•  Omnichannel POS/factory/DialogFactory.js

Note that there is currently no option to extend the App Enablement API for the Mobile Client UI5.

1.4.1.1 posHostApi.js

This is the main interface between the host (Mobile Client) and the app (client) itself. Therefore, all
communication with App Enablement is done between the posHostApi.js and the
AppEnablementConnector.js . In summary, it can be said that the posHostApi.js provides all functionalities
of the current App Enablement API and the POS features that are supported for a specific version. Versioning at
all will be supported in an upcoming version.

The following features are supported from the posHostApi.js :

App Enablement 2.0

17

•  Generation of tokens for the host (Mobile Client) and the client app so that there is a security check to only run

apps that have a valid token.

•  Checking of origins between host and client app for JavaScript postMessage() technology.
•  The IFrames in the Host that serve as a container for the client apps need to have URL encoding which is

done with plain JavaScript in two steps:
•  Encode the general URL via encodeURI().
•  Encode the HTML URL parameters that are separated by '?' and '&' via encodeURIComponent().

--> Therefore, parametrized URL GET parameters for the IFrame are supported.

1.4.1.2 AppFactory.js

This factory class is responsible to create any kind of app dynamically according to a predefined configuration.
That configuration will be explained in the next chapter. Therefore, it determines the slot in the UI where the app
is displayed, the way how the app is opened and with which dimensions.

1.4.1.3 DialogFactory.js

The Mobile Client UI5 has a dialog system to display different kinds of features. This system is also used for
App Enablement. That means all major features are displayed in a full screen dialog that uses the complete
dimension of the Mobile Client. The dialog itself serves as a container for the app which is rendered in this
container with an IFrame. The benefit of using these dialogs is that the Mobile Client keeps the control over the
client apps. Otherwise, if the app would result in an error, the complete flow of the POS would be blocked from
the UI perspective. But the dialog container is hosted by the Mobile Client and can be closed at any time.

2  Samples and Best Practises

2.1  Example App

The following example shows how to create an app and how to use the App Enablement API.

18

App Enablement 2.0

<!DOCTYPE html>
<html dir="ltr" lang="de-DE">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <script type="text/javascript" src="./libs/appEnablement/AppEnablementConnector.js"></script>
    <script type="text/javascript" src="./libs/appEnablement/api/Common.js"></script>
    <script type="text/javascript" src="./libs/appEnablement/api/Masterdata.js"></script>
    <script type="text/javascript" src="./libs/appEnablement/api/ExternalMasterdata.js"></script>
    <script type="text/javascript" src="./libs/appEnablement/api/Pos.js"></script>
    <script type="text/javascript">
      var oAppEnablementCommonInstance = new comGkSoftwareGkrAppEnablementApi.Common();
      var oAppEnablementExternalMasterdataInstance = new
comGkSoftwareGkrAppEnablementApi.ExternalMasterdata();
      var oAppEnablementMasterdataInstance = new comGkSoftwareGkrAppEnablementApi.Masterdata();
      var oAppEnablementPosInstance = new comGkSoftwareGkrAppEnablementApi.Pos();
      function good(id, val) {
        val = JSON.stringify(val);
        setHTML(id, "<div style='width:320px; color: green; font-weight: bold; word-wrap: break-word;'>OK (" +
val + ")</div>");
      }
      function fail(ID, err) {
        setHTML(id, "<div style='color: orange; font-weight: bold;'>ERR (" + err + ")</div>");
      }
      function setHTML(id, html) {
        if (document.getElementById(id) != null) {
          document.getElementById(id).innerHTML = html;
        }
      }
      // getSessionContext
      function getSessionContext() {
        oAppEnablementCommonInstance.getSessionContext('currentSessionContextFound',
'noCurrentSessionContext');
      }
      function currentSessionContextFound(context) {
        this.context = context;
        good('statusGetSessionContext', context);
      }
      function noCurrentSessionContext(err) {
        fail('statusGetSessionContext', 'FAIL(' + err + ')');
      }
    </script>
</head>
<body style="margin:0; padding:0;">
<div style="font-size:110%; font-weight:bold; padding-bottom:20px;">
GKR Example App
</div>
<table border="1" style="font-size:70%;">
    <form onsubmit="getSessionContext();" action="javascript:void(0);">
        <tr>
            <td style="width:100px;>
                <div style="font-weight: bold">getSessionContext</div>
            </td>
            <td><input type=submit value="execute" style="width: 80px; " /></td>
        </tr>
        <tr>
            <td colspan="2" id="statusGetSessionContext">
                <div style='color: red; font-weight: bold;'>---</div>
            </td>
        </tr>
    </form>
</table>
</body>
</html>

App Enablement 2.0

19

2.2  Register to barcode-scan event on the POS Client (Full Client/Thin

Client)

In case that an app needs to react to barcode-scan events, the following steps must be performed:

1.  A listener must be registered for event with ID "EVENT_POS_INPUT_SCANNER_DATA" and passData must be set

to true to retrieve the scan data message.

oAppEnablementCommonInstance.registerListener
(oAppEnablementCommonInstance.
createRegisterListenerRequest
("EVENT_POS_INPUT_SCANNER_DATA", "processBarcode", true));

2.  Implement a callback function which is called when a scan event occurs:

var processBarcode = function (scanData) {
    alert("Received scanner data: " + JSON.stringify(scanData));
};

The passed value for the scanData object has the following structure:

{
  "messageHeader" : {
    "messageKey" : "EVENT_POS_INPUT_SCANNER_DATA",
    "senderName" : null,
    "messagingStyle" : "ASYNCHRON",
    "processEventSource" : "SC",
    "recipient" : null
  },
  "payload" : "4002919000115",
  "scanData" : "NDAwMjkxOTAwMDExNQ==",
  "scanDataTypes" : [ 104 ],
  "messageKey" : "EVENT_POS_INPUT_SCANNER_DATA",
}

Code Block 1 Example message for scanned EAN13 barcode with value 4002919000115

In case that a POS version < 5.5.3 is used, the app must register on event ID "EVENT_POS_INPUT_" instead of
the one given above.

20

App Enablement 2.0

2.3  Register Internal Line Item

2.3.1 Minimal Request

{
   "itemID":"1"
}

2.3.2 Extended Request

2.3.2.1 Minimal Promotion Data

{
   "itemID":"1",
   "language":"de_DE",
   "isoCurrencyCode":"EUR",
   "customerOrderID":"3",
   "customerOrderSequenceNumber":"666",
   "salesOrderTypeCode":"20",
   "quantity":1,
   "salesOrderDeliveryTypeCode":"03",
   "requestedDeliveryDate":"2017-12-24",
   "actualUnitPrice":33.33,
   "itemType":"CO",
   "retailPriceModifierList":[
      {
         "retailPriceModifierSequenceNumber":1,
         "amount":5,
         "extendedAmountBeforeModification":33.33,
         "extendedAmountAfterModification":28.33,
         "retailTransactionPriceDerivationRule":
            {
                "promotionID":333,
                "receiptPrinterName":"Test Promotion"
            }
      }
   ],
   "lineItemExtensionList":[
      {
         "extensionKey":"TestKey",
         "extensionValue":"TestValue"
      }
   ]
}

App Enablement 2.0

21

2.3.2.2 Maximal Promotion Data

22

App Enablement 2.0

{
   "itemID":"1",
   "language":"de_DE",
   "isoCurrencyCode":"EUR",
   "customerOrderID":"3",
   "customerOrderSequenceNumber":"666",
   "salesOrderTypeCode":"20",
   "quantity":1,
   "salesOrderDeliveryTypeCode":"03",
   "requestedDeliveryDate":"2017-12-24",
   "itemType":"CO",
   "retailPriceModifierList":[
      {
         "retailPriceModifierSequenceNumber":1,
         "percent":null,
         "amount":5,
         "extendedAmountBeforeModification":33.33,
         "extendedAmountAfterModification":28.33,
         "appliedQuantity":1,
         "triggerSequenceNumber":0,
         "extraAmount":0.0,
         "roundingAmount":0.0,
         "calculationBaseAmount":0.0,
         "retailTransactionPriceDerivationRule":{
            "promotionID":333,
            "priceDerivationRuleID":334,
            "priceDerivationRuleEligibilityID":335,
            "promotionDescription":"Test Description",
            "receiptPrinterName":"Test Promotion",
            "promotionPriceDerivationRuleSequence":100,
            "promotionPriceDerivationRuleResolution":200,
            "promotionPriceDerivationRuleTypeCode":"ZRKR",
            "priceModificationMethodCode":"RP",
            "priceDerivationRuleDescription":"Test Rule Description",
            "promotionOriginatorTypeCode":"01",
            "externalPromotionID":"7777",
            "externalPriceDerivationRuleID":"7778",
            "triggerQuantity":1.0,
            "giftCertificateExpirationDate":"2017-12-24",
            "discountMethodCode":"00",
            "prohibitPrintFlag":false,
            "tenderTypeCode":"ZTPR",
            "promotionTypeName":"Test Promotion Type",
            "calculationBase":"00",
            "noEffectOnSubsequentPriceDerivationRulesFlag":false,
            "prohibitTransactionRelatedPriceDerivationRulesFlag":false,
            "couponPrintoutID" : "9959999999998",
            "couponPrintoutRule" : "00",
            "couponPrintoutText" : "<CouponPrintoutText><Line><TextLine><Text>Buy a towel
and</Text><Format>BIG</Format><Format>BOLD</Format></TextLine></Line><Line><TextLine><Text>get 10%
discount!</Text><Format>BIG</Format><Format>BOLD</Format></TextLine></Line></CouponPrintoutText>",
            "exclusiveFlag":false,
            "concurrenceControlVector":"0000000000",
            "appliedCount":1.0,
            "printoutValidityPeriod":0.0
         },
         "saleReturnLineItemPromotionTriggerList":[{
            "triggerSequenceNumber" : 0,
            "triggerType" : "CO",
            "triggerValue" : "13",
            "privilegeType" : "RS",
            "privilegeValue" : 5.0,
            "reasonCode" : "6010",
            "reasonDescription" : "Reason Description",
            "triggerSequenceAddend" : 1
         }]
      }
   ],
   "lineItemExtensionList":[
      {
         "extensionKey":"TestKey",
         "extensionValue":"TestValue"

App Enablement 2.0

23

      }
   ]
}

2.3.3 Sales Order Pickup

{
   "itemID":"1",
   "customerOrderID":"3",
   "customerOrderSequenceNumber":"666",
   "salesOrderTypeCode":"20",
   "quantity":1,
   "salesOrderDeliveryTypeCode":"03",
   "requestedDeliveryDate":"2017-12-24",
   "itemType":"PU"
}

2.4  Register External Line Item

2.4.1 Minimal Request

{
   "posItemID":"3636",
   "itemID":"4711",
   "unitOfMeasureCode":"PCE",
   "itemType":"CO",
   "actualUnitPrice":15.55,
   "quantity":1,
   "receiptText":"Test Item",
   "registrationNumber":"3636",
   "mainPOSItemID":"3636",
   "taxGroupID":"A1"
}

24

App Enablement 2.0

2.4.2 Extended Request

2.4.2.1 Minimal Promotion Data

App Enablement 2.0

25

{
   "posItemID":"3636",
   "itemID":"4711",
   "posDepartmentID":"123",
   "unitOfMeasureCode":"PCE",
   "itemType":"CO",
   "regularUnitPrice":17.99,
   "actualUnitPrice":15.55,
   "quantity":1,
   "units":1.0,
   "quantityInputMethod":"01",
   "receiptText":"Test Item",
   "receiptDescription":"Test Item Description",
   "wicFlag":true,
   "allowFoodStampFlag":true,
   "registrationNumber":"54321",
   "discountFlag":true,
   "frequentShopperPointsEligibilityFlag":true,
   "discountTypeCode":null,
   "priceChangeTypeCode":"01",
   "priceTypeCode":"01",
   "notConsideredByLoyaltyEngineFlag":false,
   "merchandiseHierarchyGroupName":"Merchandise Group Name",
   "merchandiseHierarchyGroupDescription":"Merchandise Group Description",
   "itemClassCode":"icc4",
   "prohibitTaxExemptFlag":false,
   "prohibitReturnFlag":false,
   "warrantyDuration":12,
   "depositTypeCode":"00",
   "taxExemptCode":null,
   "mainPOSItemID":"963852",
   "mainMerchandiseHierarchyGroupIDQualifier":"MAIN",
   "mainMerchandiseHierarchyGroupID":"060104",
   "taxGroupID":"A1",
   "tareCount":0.0,
   "saleReturnLineItemCharacteristicList":[
        {
            "characteristicID" : "COLOR",
            "characteristicValueID" : "1",
            "characteristicValueName" : "red"
        }
   ],
   "saleReturnLineItemMerchandiseHierarchyGroupList":[
        {
            "merchandiseHierarchyGroupIDQualifier" : "MAIN",
            "merchandiseHierarchyGroupID" : "060104"
        }
   ],
   "retailTransactionLineItemI18NTextList":[
        {
            "textSequenceNumber" : 1,
            "languageID" : "de_DE",
            "category" : "SATE",
            "text" : "Test Item Information",
            "pictureFlag" : false
        },
        {
            "textSequenceNumber" : 2,
            "languageID" : "de_DE",
            "category" : "SAIC",
            "text" : "bio_product",
            "pictureFlag" : true
        },
        {
            "textSequenceNumber" : 3,
            "languageID" : "de_DE",
            "category" : "SAIC",
            "text" : "duration_low_price",
            "pictureFlag" : true
        }
   ],
   "serializedUnitModifer":{

26

App Enablement 2.0

        "serialNumber":"SN123456"
   },
   "saleReturnLineItemSalesOrder":{
      "externalCustomerOrderID":"ID4711",
      "customerOrderSequenceNumber":97,
      "salesOrderTypeCode":"10",
      "salesOrderDeliveryTypeCode":"00",
      "requestedDeliveryDate":"2017-12-24"
   },
   "reasonCode":null,
   "reasonCodeGroupCode":null,
   "reasonDescription":null,
   "retailTransactionLineItemAdditionalParameterList":[

   ],
   "retailPriceModifierList":[
      {
         "retailPriceModifierSequenceNumber":1,
         "amount":7.55,
         "extendedAmountBeforeModification":15.55,
         "extendedAmountAfterModification":8.00,
         "retailTransactionPriceDerivationRule":{
            "promotionID":333,
            "receiptPrinterName":"Test Promotion"
         }
      }
   ],
   "lineItemExtensionList":[
      {
         "extensionKey":"TestExtension",
         "extensionValue":"TestValue"
      }
   ]
}

App Enablement 2.0

27

2.4.2.2 Maximal Promotion Data

28

App Enablement 2.0

{
   "posItemID":"3636",
   "itemID":"4711",
   "posDepartmentID":"123",
   "unitOfMeasureCode":"PCE",
   "itemType":"CO",
   "regularUnitPrice":17.99,
   "actualUnitPrice":15.55,
   "quantity":1,
   "units":1.0,
   "quantityInputMethod":"01",
   "receiptText":"Test Item",
   "receiptDescription":"Test Item Description",
   "wicFlag":true,
   "allowFoodStampFlag":true,
   "registrationNumber":"54321",
   "discountFlag":true,
   "frequentShopperPointsEligibilityFlag":true,
   "discountTypeCode":null,
   "priceChangeTypeCode":"01",
   "priceTypeCode":"01",
   "notConsideredByLoyaltyEngineFlag":false,
   "merchandiseHierarchyGroupName":"Merchandise Group Name",
   "merchandiseHierarchyGroupDescription":"Merchandise Group Description",
   "itemClassCode":"icc4",
   "prohibitTaxExemptFlag":false,
   "prohibitReturnFlag":false,
   "warrantyDuration":12,
   "depositTypeCode":"00",
   "taxExemptCode":null,
   "mainPOSItemID":"963852",
   "mainMerchandiseHierarchyGroupIDQualifier":"MAIN",
   "mainMerchandiseHierarchyGroupID":"060104",
   "taxGroupID":"A1",
   "tareCount":0.0,
   "saleReturnLineItemCharacteristicList":[
        {
            "characteristicID" : "COLOR",
            "characteristicValueID" : "1",
            "characteristicValueName" : "red"
        }
   ],
   "saleReturnLineItemMerchandiseHierarchyGroupList":[
        {
            "merchandiseHierarchyGroupIDQualifier" : "MAIN",
            "merchandiseHierarchyGroupID" : "060104"
        }
   ],
   "retailTransactionLineItemI18NTextList":[
        {
            "textSequenceNumber" : 1,
            "languageID" : "de_DE",
            "category" : "SATE",
            "text" : "Test Item Information",
            "pictureFlag" : false
        },
        {
            "textSequenceNumber" : 2,
            "languageID" : "de_DE",
            "category" : "SAIC",
            "text" : "bio_product",
            "pictureFlag" : true
        },
        {
            "textSequenceNumber" : 3,
            "languageID" : "de_DE",
            "category" : "SAIC",
            "text" : "duration_low_price",
            "pictureFlag" : true
        }
   ],
   "serializedUnitModifer":{

App Enablement 2.0

29

        "serialNumber":"SN123456"
   },
   "saleReturnLineItemSalesOrder":{
      "externalCustomerOrderID":"ID4711",
      "customerOrderSequenceNumber":97,
      "salesOrderTypeCode":"10",
      "salesOrderDeliveryTypeCode":"00",
      "requestedDeliveryDate":"2017-12-24"
   },
   "reasonCode":null,
   "reasonCodeGroupCode":null,
   "reasonDescription":null,
   "retailTransactionLineItemAdditionalParameterList":[

   ],
   "retailPriceModifierList":[
      {
         "retailPriceModifierSequenceNumber":1,
         "percent":null,
         "amount":7.55,
         "extendedAmountBeforeModification":15.55,
         "extendedAmountAfterModification":8.00,
         "appliedQuantity":1,
         "triggerSequenceNumber":0,
         "extraAmount":0.0,
         "roundingAmount":0.0,
         "calculationBaseAmount":0.0,
         "retailTransactionPriceDerivationRule":{
            "promotionID":333,
            "priceDerivationRuleID":334,
            "priceDerivationRuleEligibilityID":335,
            "promotionDescription":"Test Description",
            "receiptPrinterName":"Test Promotion",
            "promotionPriceDerivationRuleSequence":100,
            "promotionPriceDerivationRuleResolution":200,
            "promotionPriceDerivationRuleTypeCode":"ZRKR",
            "priceModificationMethodCode":"RP",
            "priceDerivationRuleDescription":"Test Rule Description",
            "promotionOriginatorTypeCode":"01",
            "externalPromotionID":"7777",
            "externalPriceDerivationRuleID":"7778",
            "triggerQuantity":1.0,
            "giftCertificateExpirationDate":"2017-12-24",
            "discountMethodCode":"00",
            "prohibitPrintFlag":false,
            "tenderTypeCode":"ZTPR",
            "promotionTypeName":"Test Promotion Type",
            "calculationBase":"00",
            "noEffectOnSubsequentPriceDerivationRulesFlag":false,
            "prohibitTransactionRelatedPriceDerivationRulesFlag":false,
            "couponPrintoutID" : "9959999999998",
            "couponPrintoutRule" : "00",
            "couponPrintoutText" : "<CouponPrintoutText><Line><TextLine><Text>Buy a towel
and</Text><Format>BIG</Format><Format>BOLD</Format></TextLine></Line><Line><TextLine><Text>get 10%
discount!</Text><Format>BIG</Format><Format>BOLD</Format></TextLine></Line></CouponPrintoutText>",
            "exclusiveFlag":false,
            "concurrenceControlVector":"0000000000",
            "appliedCount":1.0,
            "printoutValidityPeriod":0.0
         },
         "saleReturnLineItemPromotionTriggerList":[{
            "triggerSequenceNumber" : 0,
            "triggerType" : "CO",
            "triggerValue" : "13",
            "privilegeType" : "RS",
            "privilegeValue" : 5.0,
            "reasonCode" : "6010",
            "reasonDescription" : "Reason Description",
            "triggerSequenceAddend" : 1
         }]
      }
   ],

30

App Enablement 2.0

   "lineItemExtensionList":[
      {
         "extensionKey":"TestExtension",
         "extensionValue":"TestValue"
      }
   ]
}

2.4.3 Pay-in Line Item

{
   "itemType":"PI",
   "actualUnitPrice":15.55,
   "quantity":1,
   "reasonCode" : "6301",
   "reasonCodeGroupCode" : "E",
   "reasonDescription" : "Pay-in Reason Description",
   "retailTransactionLineItemAdditionalParameterList":[
    {
        "externalParameterID":"A1",
        "parameterName":"Additional Parameter",
        "parameterValue":"Value"
    }
   ]
}

2.4.4 Pay-out Line Item

{
   "itemType":"PO",
   "actualUnitPrice":15.55,
   "quantity":1,
   "reasonCode" : "6401",
   "reasonCodeGroupCode" : "A",
   "reasonDescription" : "Pay-out Reason Description",
   "retailTransactionLineItemAdditionalParameterList":[
    {
        "externalParameterID":"A1",
        "parameterName":"Additional Parameter",
        "parameterValue":"Value"
    }
   ]
}

App Enablement 2.0

31

2.4.5 Sales Order Pickup

{
   "posItemID":"3636",
   "itemID":"4711",
   "unitOfMeasureCode":"PCE",
   "itemType":"PU",
   "actualUnitPrice":15.55,
   "quantity":1,
   "receiptText":"Test Item",
   "registrationNumber":"3636",
   "mainPOSItemID":"3636",
   "taxGroupID":"A1",
   "saleReturnLineItemSalesOrder":{
      "externalCustomerOrderID":"ID4711",
      "customerOrderSequenceNumber":97,
      "salesOrderTypeCode":"10",
      "salesOrderDeliveryTypeCode":"00",
      "requestedDeliveryDate":"2017-12-24"
   }
}

2.4.6 Down Payment Clearing

{
   "itemType":"DC",
   "actualUnitPrice":15.55,
   "quantity":1,
   "saleReturnLineItemSalesOrder":{
      "externalCustomerOrderID":"ID4711",
      "customerOrderSequenceNumber":97,
      "salesOrderTypeCode":"10",
      "salesOrderDeliveryTypeCode":"00",
      "requestedDeliveryDate":"2017-12-24"
   }
}

2.5  Cancel Current Transaction

2.5.1 Minimal Request

{ }

2.5.2 Maximal Request

{
   "reasonCode":"CTNMC",
   "reasonDescription":"No money"
}

32

App Enablement 2.0

2.6  Register Customer

2.6.1 Minimal Request

{
   "customerId":"10065"
}

2.6.2 Maximal Request

{
   "customerId":"10065",
   "customerServiceTypeCode":"SAP_ERP",
   "preferredReceiptPrintoutTypeCode":"PRINTANDMAIL"
}

2.7  Create Transaction Extension

{
   "extensionKey":"txKey1",
   "extensionValue":"txValue1"
}

2.8  Update Transaction Extension

{
   "extensionKey":"txKey1",
   "extensionValue":"txValue2"
}

2.9  Delete Transaction Extension

{
   "extensionKey":"txKey1"
}

App Enablement 2.0

33

2.10  Add Printout Data

2.10.1 Register Internal Line Item with Additional Printout Data

{
   "itemID":"1",
   "printAdditionalLineItemTextLineList": [{
        "text" : "AFTER AFTER AFTER",
        "sortOrder":"afterLineItem",
        "styleID":"NormalPlain"
    },
    {
        "text" : "BEFORE BEFORE BEFORE",
        "sortOrder":"beforeLineItem",
        "styleID":"NormalPlain"
    }]
}

2.10.2 Register External Line Item with Additional Printout Data

{
   "posItemID":"3636",
   "itemID":"4711",
   "unitOfMeasureCode":"PCE",
   "itemType":"CO",
   "actualUnitPrice":15.55,
   "quantity":1,
   "receiptText":"Test Item",
   "registrationNumber":"3636",
   "mainPOSItemID":"3636",
   "taxGroupID":"A1",
    "printAdditionalLineItemTextLineList": [{
        "text" : "AFTER AFTER AFTER",
        "sortOrder":"afterLineItem",
        "styleID":"NormalPlain"
    },
    {
        "text" : "BEFORE BEFORE BEFORE",
        "sortOrder":"beforeLineItem",
        "styleID":"NormalPlain"
    }]
}

2.10.3 Add Additional Transaction Report

{
    "reportIdentification" : "AppReport",
    "printAdditionalLineItemTextLineList" : [ {
            "text" : "Example Text Line 1",
            "sortOrder" : "",
            "styleID" : "NormalPlain"
        },
        {
            "text" : "Example Text Line 2",
            "sortOrder" : "",
            "styleID" : "NormalPlain"
        }
    ]
}

Contact

GK SOFTWARE SE
Waldstraße 7
08261 Schöneck
Germany

Tel.:  +49 (0) 3 74 64 84 – 0
Fax:  +49 (0) 3 74 64 84 – 15

Email: documentation@gk-software.com
www.gk-software.com

