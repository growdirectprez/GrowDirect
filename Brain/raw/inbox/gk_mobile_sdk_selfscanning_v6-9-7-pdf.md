---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/tier1-md/gk-pos/GK_Mobile_SDK_Selfscanning_v6.9.7.pdf.md
tags: [canary, gk-pos, fujitsu, reference, benchmark, tier1-extract]
project: canary
status: unprocessed
---

# GK_Mobile_SDK_Selfscanning_v6.9.7.pdf

## Source
File: `Brain/raw/.extract/tier1-md/gk-pos/GK_Mobile_SDK_Selfscanning_v6.9.7.pdf.md`
Size: 87,225 bytes

## Raw content
SAP Mobile Consumer Assistant by GK

OmniPOS Mobile SDK for Self Scanning

Version: 6.9.7

Copyright

© 2018 SAP SE or an SAP affiliate company. All rights reserved. No part of this publication may be

reproduced or transmitted in any form or for any purpose without the express permission of SAP SE or

an SAP affiliate company.

1.  You may not use the SAP Material for a purpose competitive with SAP or its products unless

otherwise clearly permitted by applicable law.

2.  You may not use the SAP corporate logo.

3.  No use of other SAP trademarks is granted under this section. For information regarding use of

SAP trademarks, see http://www.sap.com/corporate/en/legal/trademark.html.

SAP and other SAP products and services mentioned herein as well as their respective logos are

trademarks or registered trademarks of SAP SE (or an SAP affiliate company) in Germany and other

countries. All other product and service names mentioned are the trademarks of their respective

companies.

Contents

General .................................................................................................................................... 5

Requirements and Setup ..................................................................................................... 6

iOS SDK ............................................................................................................................................................................... 6

Technical requirements ......................................................................................................................................................... 6
Setup - Using the SDK in existing iOS applications ...................................................................................................... 6

Android SDK ...................................................................................................................................................................... 7

Technical requirements ......................................................................................................................................................... 8
Setup - Using the SDK in existing Android applications............................................................................................. 8

SDK Layers and Communication....................................................................................... 10

General Workflows ............................................................................................................... 12

Lifecycle of the Self Scanning process ...................................................................................................................... 12

Line item operations ...................................................................................................................................................... 13

Analyze item barcode ........................................................................................................................................................... 13
Add item to transaction ........................................................................................................................................................ 13
Remove item from transaction........................................................................................................................................... 15
Change quantity of an item ................................................................................................................................................ 15

Most common transaction and line item properties ............................................................................................. 16

Special Workflows ................................................................................................................ 21

Recovering a transaction .............................................................................................................................................. 21

Sales restriction: Age ..................................................................................................................................................... 21

Sales restriction: Security items ...................................................................................................................................22

Scan items with special quantity requirements .......................................................................................................23

SDK Methods ........................................................................................................................ 25

Method Overview ...........................................................................................................................................................25

Method Setup .................................................................................................................................................................26

Method StartSelfscanningSession ..............................................................................................................................26

Method EndSelfscanningSession ................................................................................................................................28

Method RegisterLineItem .............................................................................................................................................29

Method ProcessBarcode ...............................................................................................................................................30

Method SetQuantity ......................................................................................................................................................32

Method VoidLineItem .................................................................................................................................................. 34

Method AnalyzeBarcode ..............................................................................................................................................35

Method GetTransaction ................................................................................................................................................36

Method CreateTransaction .......................................................................................................................................... 37

Method CancelTransaction ..........................................................................................................................................38

Method RecoverTransaction........................................................................................................................................39

Error Codes ........................................................................................................................... 41

List of abbreviations ............................................................................................................ 62

General

General

5

GK Software is a leading provider of retail applications for real-time Omnichannel business.

As one module of these applications, the Mobile SDK for Self Scanning allows customers the

integration and usage of the GK POS Interfaces. During the Self Scanning process, customers can scan

item barcodes on their own and put them into the shopping cart. An additional scan by the cashier is

no longer necessary, which saves time and is more comfortable for the customer. In addition, the

customer is always informed about the sum of the transaction and also about item discounts.

Self Scanning itself can be performed in two ways:

  by using an industrial device which is provided to the customers within the shops

  by using the own devices of the customers (BYOD - Bring your own device)

This documentation is generated for the BYOD case. Typically, the Mobile SDK for Self Scanning will be

integrated into existing native applications to extend the functionality of these applications. The SDK

contains the interfaces to communicate with the GK/Retail POS and manage the Self Scanning process.

The following chapters describe in a detail way the system requirements to implement the SDK, how to

implement the SDK and how the processes are working. The second part of this documentation

describes more technical details about the available methods, in addition a list of error codes is

provided.

 6

Requirements and Setup

Requirements and Setup

iOS SDK

The Mobile SDK for Self Scanning can be used for integrating the Self Scanning feature into native

applications for iOS and Android. The following chapter describes the minimum platform requirements

for the SDK and how to integrate it into an existing iOS application.

Technical requirements

IDE

iOS SDK

Valid Architectures

Compatible languages

Minimum requirement

Xcode 9.2 or newer

Latest (10.0 or newer)

i386

x86_64

armv7

armv7s

arm64

ObjC

Swift

Setup - Using the SDK in existing iOS applications

Step  Description

Details

1

Link the SDK library
(SelfscanSDK.a)
and all header files
to your project.

Requirements and Setup

Step  Description

Details

2

Add the following
Other Linker Flags

-ObjC

-fprofile-instr-
generate

7

3

Import
SelfscanSDK.h
header file

For more information about Bridging Headers, see
https://developer.apple.com/library/content/documentation/Swift/Conceptual/BuildingCocoaA
pps/MixandMatch.html

Note: For Swift
projects, the
SelfscanSDK.h
must be imported
within the Bridging-
Header.h file. In
case a Bridging
Header is needed, it
must be declared in
the Build Settings of
the project.

4

Set up the SDK by
calling the Setup
method and specify
a URL where the
POS Service can be
reached. For more
details, check the
method descriptions
in the following
chapters.

Android SDK

The Mobile SDK for Self Scanning can be used for integrating the Self Scanning feature into native

applications for iOS and Android. The following chapter will describe the minimum platform

requirements for the SDK and how to integrate this into existing Android applications.

Requirements and Setup

 8

Technical requirements

IDE

Android Studio 3.0 or newer recommend

Minimum requirement

Android SDK

14 or newer

Compatible languages

Java, Kotlin

Setup - Using the SDK in existing Android applications

Step Description

Details

1

Copy and link the SDK
library (SelfscanSDK aar
file) to the libs folder of the
project.

2  When using Gradle, add

the Self Scanning SDK as
dependency to the
app/build.gradle

repositories {
    flatDir {
        dirs 'libs'
     }
}

...

Gradle >= 3
implementation(name:
'SelfscanSDK-1.0.0', ext:
'aar')
Gradle < 3
compile(name:
'SelfscanSDK-1.0.0', ext:
'aar')

Requirements and Setup

Step Description

Details

3

Set up the SDK by calling
the Setup method and
specify a URL where the
POS service can be
reached. For more details,
check the method
descriptions in the
following chapters.

9

 10

SDK Layers and Communication

SDK Layers and Communication

The Mobile SDK for Self Scanning makes the communication with the POS Service easier and the

implementation faster. It is recommend using only the SelfscanSDK main methods for the

communication. Nevertheless, the SDK also allows to use the POS Service APIs directly, if necessary.

Within the SDK there are three main layers:

1.  The SelfscanSDK main layer: It contains all necessary methods and parameters to communicate

to the POS Service.

2.  The SDK API layer: The connection between the main and the POS Service API layer contains

minor logic and simplifications to make the communication to the POS Service easier.
3.  The POS Service API layer is the direct connection to the POS Service. All methods that are

provided by the POS services are located within this layer.

By using the main layer, the SDK will always return an object of type SelfscanSDKResponse. This object

unifies the responses of all methods. In the following, the main properties of a SelfscanSDKResponse

are presented.

SDK Layers and Communication

11

Parameter

Description

Returned by method



operationStatus

General status whether the request was done
with success or not. The value is filled by the
POS Service.



all

  OK
  NOK



statusCode

The HTTPS status of the response that the SDK
gets from the POS Service.



all



transactionOperationResult

Complex type that contains the most important
properties for all item operations:







transaction - transaction including all
line items
addedOrdModifiedLineItems - list of
items that has been changed during last
operation
registrationDetails - details about
additional item information that is
required (for example, quantity
information)







registerLineItem
processBarcode
voidLineItem
setQuantity/setPieces
getTransaction



analyzeBarcodeResponse

Contains detailed information about the barcode
analysis, like line item operation.



analyzeBarcode



errorResponse

Contains detailed information about the returned
error from the POS Service. If there is no error,
the property is not set.



all



suspendNumber

The suspend number contains an identifier for
the parked transaction at the Backoffice server. It
can be used later on for the payment process at
the POS.



endSelfscanningSession

 12

General Workflows

Lifecycle of the Self Scanning process

General Workflows

This chapter gives an overview about the lifecycle of a typical Self Scanning process.

From a user’s perspective, the lifecycle starts with entering a shop and opening the Self Scanning

application on a mobile device. Afterwards, the customer goes through the market and puts some

articles into the shopping cart. Each item has a barcode which the customer scans with the mobile

application. The mobile app will display the scanned items in a virtual shopping cart including price and

discount information.

When the customer finishes scanning all items, the next step is the checkout. For this, a checkout

number is displayed at the mobile device of the customer which can be scanned by a cashier. The

checkout number can be displayed in any format, for example, as a QR code. Afterwards, the cashier


## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
