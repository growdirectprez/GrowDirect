---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/tier1-md/gk-pos/GK_AppEnablement-2.0_v516.pdf.md
tags: [canary, gk-pos, fujitsu, reference, benchmark, tier1-extract]
project: canary
status: unprocessed
---

# GK_AppEnablement-2.0_v516.pdf

## Source
File: `Brain/raw/.extract/tier1-md/gk-pos/GK_AppEnablement-2.0_v516.pdf.md`
Size: 66,030 bytes

## Raw content
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

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
