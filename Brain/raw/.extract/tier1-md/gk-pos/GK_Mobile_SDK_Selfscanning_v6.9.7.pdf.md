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

immediately gets the full transaction including sum of the customer displayed without scanning all the

items again. So only the payment itself is left which can be done by cash or any tender type.

From a more technical perspective, the lifecycle also starts with entering a shop. The mobile application

with the SDK for Self Scanning has to know how to connect to the POS Service. Normally, the shop

provides a Wi-Fi network to which the customer has to connect the mobile device. After connecting,

the POS Service can be reached by a given URL or IP address. If there is a central POS Service, it can be

reached without any Wi-Fi restriction. The mobile application now has to create a session (with a given

user id) and an empty transaction. The transaction is used to hold the status of all articles the customer

wants to buy. These articles will be scanned by the camera of the mobile device. Technical, the scanned

barcode (for example, EAN13) will be sent to the POS Service to identify the item. Afterwards, it can be

added to the shopping cart, which means the transaction will contain this single item with all item

information which is necessary for the customer: title, short description, price and so on. More item

operations like this can be done from the mobile application via the SDK: change the quantity of

existing items, remove items from the transaction.

When the customer has collected all items, the Self Scanning process can be finished. For this purpose,

the session can be ended. This means the transaction is saved at the Backoffice server of the retailer. A

parking or suspend number will identify this saved transaction - the POS Service will return this

suspend number to the mobile device, that has to display the parking number in any style. When the

cashier scans the suspend number, the transaction will be fetched from the Backoffice server to the

POS and all details get displayed to the cashier for the payment process.

General Workflows

13

In the graphic above, the lifecycle of a typical Self Scanning procedure is displayed.

  The upper line shows the customer perspective.

  The middle line shows a more technical perspective of a session.

  The bottom line shows the methods of the SDK, which perform the action.

Note: CreateTransaction is not necessary to call. In case a lineItem will be registered and no transaction

exists yet, the POS Service will create a transaction automatically.

Line item operations

Analyze item barcode
During the Self Scanning process, there might be cases where an analysis of the barcode is necessary.

This could,for example, be the case for gift cards which are no standard items. The SDK provides two

methods to analyze a barcode:

  analyzeBarcode

The analyzeBarcode method requires a barcode as request parameter. The POS Service will return

possible actions for the scanned barcode afterwards. These actions are identified by a given barcode

rule of the POS Service. The action is independent from whether the item is part of the master data or

not - it just identifies the barcode as mentioned.

Details of the analyzeBarcode response are described in the following method chapter.

Note: Items that cannot by analyzed cannot be added to the shopping card - the POS Service will

return an exception.

Note: It is recommend using the processBarcode method instead of analyzeBarcode. For more

information, see next chapter about adding items to a transaction.

Add item to transaction
The most common process of a Selfscan procedure is adding items to the shopping cart. The SDK

provides two methods to do this:

 14

General Workflows



registerLineItem

  processBarcode



registerLineItemWithQuantityValidation

The registerLineItem adds an item by a given barcode to the transaction. There is no complex logic

behind it: In case of any error, the item will not be added and the SDK will return the error from the

POS Service. When no error occurs, the POS Service response will contain the updated transaction

including the new added item.

The second way how to add an item to a transaction is by using the method processBarcode. It is the

recommend way to do this. ProcessBarcode does not just add the item to the transaction, it will also do

some analyzation and provide additional information/actions to the barcode. When the returned

operationStatus is ok, the item simply was added to the transaction. When the status is not ok, the POS

Service might have returned more details about missing requirements:

For this, the registrationDetails of the response can be checked. It will contain information about the

item name, price, and also information about the required quantity input. This means the item needs

specific quantities like length and width to be registered. The uomCode property will contain the unit.

A list of all possible quantity inputs can be found in the method section below.

Both methods, registerLineItem and processBarcode, will add new items to the transaction. In case an

item already exists in the shopping cart, the item is added a second time.

The method registerLineItemWithQuantityValidation will check whether an item with a given barcode

already exists in the transaction. If it is the case, the method will call setQuantity by increasing the

quantity by one. Otherwise, registerLineItem will be called to add the item to the transaction. The

method does not care about special quantity input requirements or items that only allow a quantity of

1 (for example, items with a special discount).

General Workflows

15

Remove item from transaction
To remove an item from a transaction, the following method should be used:

  voidLineItem

The item is removed independent of its quantity.

Change quantity of an item
A normal case of an item operation is changing the quantity of the item. The Mobile SDK for Self

Scanning provides two methods to do this:





setQuantity

setPieces

setQuantity is the default method to do this. It requires an object of type (SWG)QuantityInputSSC

which contains information like piece, length, and width. For most items only piece is important, so the

method setPieces could be used instead.

A typical case for a quantity change could be scanning a barcode a second time. So instead of adding

the item a second time to the transaction, the quantity (piece) of the existing item is increased by 1.

Note: The method registerLineItemWithQuantityValidation checks automatically whether an item

already exists within a transaction.

 16

General Workflows

Most common transaction and line item properties

Type

Property

Description

Sample response of POS Service

General

addedOrdModifiedLineItems  List of items that has been

added or modified during
the last operation. This
property can be used to
figure out which item was,
for example, added to a
transaction in the last
operation.

{

"operationStatus": "OK",
"transaction": {

Contains specific
information about items,
like special quantity
requirements or sales
restrictions. Typically, it is
not relevant for normal
transaction operation. See
processBarcode for more
information on this.

A code to denote the type
of retail transaction line
item, such as Sale/Return,
Void, Tender ...

"businessUnitGroupID":

"100000000000000110",

"transactionID":

"56l25ffb011056f41afb8eec8979843f
",

"sequenceNumber": 1,

"beginDateTimestamp":
"2018-05-23 07:38:51.621",

"retailTransactionLineItems

": [{

"key": {

registrationDetails

retailTransactionLineItemTyp
eCode

Transaction

businessUnitGroupID

Id of business unit group /
shop group. Provided by
the POS

"businessUnitGroupID":

"100000000000000110",

transactionID

sequenceNumber

Id of the current
transaction. Provided by
the POS.

The sequence number of
the transaction
(incremental number for
each workstation). It is
formatted according to
minimum and maximum
value and it could be reset
every day to minimum
value. So in comparison to
InternalSequenceNumber,
it does not have to be
unique for business unit
and workstation. It is used
for export, reporting,
search, and display.

"transactionID":

"56l25ffb011056f41afb8eec8979843f
",

"retailTransactionLineItemS

equenceNumber": 0

},

"retailTransactionLineItemT

ypeCode": "SR",

"voidFlag":

false,

"saleReturnLineItem": {

"retailTransactionLineItemS

equenceNumber": 0,

If not used, it is -1.

"mainPOSItemID":

"300026682",

beginDateTimestamp

Date and time stamp
when the transaction was
created.

"itemID": "300026682",

General Workflows

17

Type

Property

Description

Sample response of POS Service

retailTransactionLineItems

subtotal

subtotalDiscount

total

discountTotal

bonusPointsTotal

validationCode

isocurrencyCode

List of all items that are
within the transaction of
the current session.

The monetary value of the
transaction subtotal
without transaction
discounts.

The monetary value of the
transaction subtotal with
transaction discounts.

The monetary value of the
transaction total (includes
taxes that are not included
in prices).

Sum of all discounts at the
transaction.

Sum of collected bonus
points.

Not relevant - only used
for specific projects.

Currency code of the
current transaction, for
example EUR.

LineItem

retailTransactionLineItemSeq
uenceNumber

Id or index of line item
within transaction.

mainPOSItemID

itemID

In case of different item
versions, this id contains
the reference to the main
item.

Alphanumeric key that
identifies the item
uniquely.

"unitOfMeasureCode": "PCE",

"itemType": "CO",

"regularUnitPrice": 58.4,

"actualUnitPrice": 58.4,

"quantity": 1,

"units": 1.0,

"extendedAmount": 58.4,

"extendedDiscountAmount":

0.0,

"grandExtendedAmount":

58.4,

"manualWeightInputFlag":

false,

"receiptText": "Slip On

Vans Classic Slip on black whi",

"registrationNumber":

"2050600003398",

"negativeLineItemFlag":

false,

"discountFlag": true,

"frequentShopperPointsEligi

bilityFlag": true,

"prohibitReturnFlag":

false,

unitOfMeasureCode

Unit of the item.

"taxReceiptPrintCode": "C",

itemType

A code to denote the type
of retail transaction line
item, such as Sale/Return,
Void, Tender ...

"taxGroupID": "A2",

"originalTaxGroupID": "A2",

"retailPriceModifierList":

regularUnitPrice

Normal list price of an item
unit.

 18

General Workflows

Type

Property

Description

Sample response of POS Service

actualUnitPrice

Current price of an item
unit

[],

quantity

extendedAmount

extendedDiscountAmount

  PCE (piece)


...

"frequentShopperPointsModif

ierList": [],

Simplified quantity of an
item.

The product of multiplying
Quantity, Units, and
ActualUnitPrice.

The monetary total of all
line item discounts that
were applied to this Item.

"positemID":

"2050600003398"

},

"retailTransactionLineItemA

ssociationList": []

}],

"retailTransactionCouponSum

mary": [],

"retailTransactionCustomer"

grandExtendedAmount

The line item total
including taxes and
discounts.

: [{

"1",

"customerID":

manualWeightInputFlag

This flag describes, if the
weight was measured
manually.

"addressTypeCode": "CO"

}],
"subtotal": 58.4,
"subtotalDiscount":

receiptText

Text that will be displayed
at the receipt.

58.4,

registrationNumber

Typically the barcode of
the item.

negativeLineItemFlag

This flag is set for special
line items with negative
amounts. It is used to
differ between return
items.

0.0,

0.0,

"0",

"EUR"

"total": 58.4,
"discountTotal":

"bonusPointsTotal":

"validationCode":

"isocurrencyCode":

discountFlag

A flag to indicate whether
this ITEM can be
discounted.

: [{

},
"addedOrdModifiedLineItems"

"key": {

frequentShopperPointsEligibil
ityFlag

A flag to denote that the
Item is eligible for frequent
shopper points.

"businessUnitGroupID":

"100000000000000110",

prohibitReturnFlag

A flag to denote whether
this item may be returned.

"56l25ffb011056f41afb8eec8979843f
",

"transactionID":

taxReceiptPrintCode

A short code that is
printed on a receipt to
denote items that are in
this TaxableGroup.

"retailTransactionLineItemS

equenceNumber": 0

General Workflows

19

Type

Property

Description

Sample response of POS Service

taxGroupID

originalTaxGroupID

The id of the taxable
TaxableGroup.

The original id of the
taxable group.

positemID

The ID used to identify the
item. Typically the
barcode is within this
property.

},

"retailTransactionLineItemT

ypeCode": "SR",

"voidFlag": false,

"saleReturnLineItem": {

"retailTransactionLineItemS

equenceNumber": 0,

"mainPOSItemID":

Registration
Details

mainPOSItemId

Item id given by the POS
(reference to main item in
case of any sub items)

"300026682",

"300026682",

"itemID":

itemName

Name of the item.

usedBarcode

Barcode that was used
during the request.

price

Price of the item.

salesRestrictions

SalesRestrictionInfo
contain information about
special sales rules.

1,

"unitOfMeasureCode": "PCE",

"itemType":

"CO",

"regularUnitPrice": 58.4,

"actualUnitPrice": 58.4,

"quantity":

"units": 1.0,

Sales restriction type
code, for example

* AGE => Age (customer
age is to be checked)
* TIME => Sales
Prohibition Period (sale is
prohibited during specified
time)
* LIMT => Limit (maximally
this count of the item may
be sold)
* WGHT => Weight (the
weight is to be checked)
* RISK => Risk (the sale
of that item is to be
double-checked)
* - is mandatory

The value of the sales
restriction depends on the
SalesRestrictionTypeCode
, for example * Age =>
minimum customer age
* Sales Prohibition Period
=> time group ident
* Limit => limit count
* EAS tag => type of the
tag, possible values: 00 =
soft tag, 01 = hard tag

"extendedAmount": 58.4,

"extendedDiscountAmount":

0.0,

"grandExtendedAmount":

58.4,

"manualWeightInputFlag":

false,

"receiptText": "Slip On

Vans Classic Slip on black whi",

"registrationNumber":

"2050600003398",

"negativeLineItemFlag":

false,

"discountFlag": true,

"frequentShopperPointsEligi

bilityFlag": true,

 20

General Workflows

Type

Property

Description

Sample response of POS Service

forceQuantityInput

quantityInputMethod

Contains if the item needs
additional quantity
information before it can
be added to the
transaction. To add an
item with a special
quantity input, the
registerLineItem method.

Contains which additional
quantity information is
needed before it can be
added to the transaction

LENGTH(02)

  PIECE(01)

  AREA(03)
  VOLUME_SPAC

E(04)

  WEIGHT(05)
  QUANTITY_AUT
OMATIC(06)
  QUANTITY_MAN

UAL(07)

uomCode

Unit of measurement of
the item - typical values
are

  ST
  KG
  KAR

LFM
  M
  M2
  M3
  ROL

"prohibitReturnFlag":

false,

"taxReceiptPrintCode": "C",
"taxGroupID":

"A2",

"originalTaxGroupID": "A2",

"retailPriceModifierList":

[],

"frequentShopperPointsModif

ierList": [],

"2050600003398"
},

"positemID":

"retailTransactionLineItemA

ssociationList": []

}],
"actions": [],
"closedLineItems": [],
"deletedLineItems": [],
"registrationDetails": {
"mainPOSItemId":

"300026682",

"prepaidItem":

"hasLinkedItems":

false,

false,

"variantItemsAvailable":

false,

false,

"emptiesReturn":

"hasInvalidQuantity":

false,

[],

"price": 0.0,
"salesRestrictions":

"forceQuantityInput":

false,

}

}

"uomCode": "PCE"

Special Workflows

Special Workflows

Recovering a transaction

21

One scenario of a Self Scanning workflow is to recover a transaction. This is, for example, necessary

when the customer ended the session (finished the Selfscan process) but wants to change something

within the shopping cart afterwards.

To recover a transaction, the recoverTransaction method can be used. The method requires an active

session which is created automatically in case it does no longer exist yet. So a createTransaction

request is not necessary. The SDK uses all given parameters for the internal start session request

(customer number, businessUnit id and so on). To change these values for the recover process, simply

overwrite the properties of the SelfscanSDK main class shared instance.

Sales restriction: Age

Many items have sales restrictions. This means it is not allowed to sell these items to children or

persons that are younger than a given age. Samples are alcohol or cigarettes. The sales restrictions

might differ from country to country.

In case of an age restriction, the SDK will provide this information within the RegistrationDetails after

registering an item (the sample shows an AGE restriction with a min age of 18 years):

"registrationDetails": {
 "mainPOSItemId": "42250715",
 "prepaidItem": false,
 "hasLinkedItems": false,
 "variantItemsAvailable": false,
 "emptiesReturn": false,

 22

Special Workflows

 "hasInvalidQuantity": false,
 "price": 0.0,
 "salesRestrictions": [{
 "salesRestrictionTypeCode": "AGE",
 "salesRestrictionValue": "18",
 "questionTypeCode": "01"
 }],
 "forceQuantityInput": false,
 "uomCode": "PCE"
 }

When the SDK returns an age restriction, it is up to the app to inform the customer about it. The age

can be validated, for example, during checkout from a cashier.

Sales restriction: Security items

Another use case is the scanning with a special risk like gift cards. Also for these items the POS Service

informs the SDK within the RegistrationDetails:

"registrationDetails": {

"mainPOSItemId": "325065",
"prepaidItem": false,
"hasLinkedItems": false,
"variantItemsAvailable": false,
"emptiesReturn": false,
"hasInvalidQuantity": false,
"price": 0.0,
"salesRestrictions": [{

"salesRestrictionTypeCode": "RISK",
"questionTypeCode": "00"

}],
"forceQuantityInput": false,
"uomCode": "PCE"

}

When the SDK returns a risk restriction, it is up to the app to inform the customer about it. The risk

item can be validated, for example, during checkout from a cashier.

Special Workflows

23

Scan items with special quantity requirements

Some items may require additional quantity information before they can be added to the shopping

cart. These can be, for example, weight items, yard goods, or items where square meters are paid, like

tilings.

The SDK will also return the additional requirements in the response of the processBarcode or

registerLineItem method. The operation status is always NOK - the item cannot be added without these

missing information.

So after taking note of such an item, the user should be asked to enter the missing quantity

information. In the sample afterwards, the POS Service is asking for a volume - so three parameters are

required.

{

"operationStatus": "NOK",
"statusCode": "GKR-200500",
"addedOrdModifiedLineItems": [],
"actions": [],
"closedLineItems": [],
"deletedLineItems": [],
"registrationDetails": {

"mainPOSItemId": "4005014313890",
"itemName": "Softwood, chamber-dried",
"usedBarcode": "4005014313890",
"prepaidItem": false,
"hasLinkedItems": false,
"variantItemsAvailable": false,
"emptiesReturn": false,
"hasInvalidQuantity": false,
"price": 1.38,
"salesRestrictions": [],
"forceQuantityInput": true,
"quantityInputMethod": "04",
"uomCode": "M3"

}

}

 24

Special Workflows

After the missing parameters are entered by the customer, the mobile app can again try to add the

item to the transaction by sending the quantity parameters within the SWGQuantityInputSSC object of

the request.

SDK Methods

SDK Methods

Method Overview

Type

iOS

Initialization setup

25

Android

Short description

setup

Initialize the SDK with a URL
to reach the POS Service.

Session
handling

startSelfscanningSessionWithCustomerNumber

startSelfscanningSessio
n

Begin a session for Self
Scanning. A customer number
is needed for this.

endSelfscanningSessionWithCompleteBlock

endSelfscanningSession  End a session by parking the
transaction at the Backoffice
server of the POS.

Transaction
handling

getTransactionWithCompleteBlock

getTransaction

createTransactionWithCompleteBlock

createTransaction

Get the current shopping cart
including all items, prices and
discounts.

Create a new shopping cart
for a customer.

cancelTransactionWithCompleteBlock

cancelTransaction

Cancel a purchase.

recoverTransactionWithCompleteBlock

recoverTransaction

Barcode
processing

analyzeBarcodeWithBarcode

analyzeBarcode

processBarcodeWithBarcode

processBarcode

Item
operations

registerLineItemWithBarcode

registerLineItem

registerLineItemWithQuantityValidationAndBarcod
e

registerLineItemWithQua
ntityValidation

setQuantity

setQuantity

Restore a canceled or ended
purchase.

Get the type of an object
behind a barcode (identify it),
like item or gift card.

Get the type of an object
behind a barcode (identify it)
and add the item to the
current transaction.

Add an item with a given
barcode to the current
shopping cart.

Add an item with a given
barcode to the current
shopping cart. In case the
item already exists, the
quantity is changed instead of
adding it another time.

Change the quantity of a
specific item, which is already
present in the shopping cart.
The quantity itself might

 26

SDK Methods

Type

iOS

Android

Short description

setPieces

setPieces

voidLineItem

voidLineItem

contain complex properties,
like length, width, weight.

Change the simple quantity of
a specific item. A use case is,
for example, changing the
quantity from 1 to 2.

Removes an item from a
shopping cart, independent
from the quantity of the item.

Method Setup

The initialization of the Mobile SDK for Self Scanning is always the first step before it can be used.

Within this step, the SDK will create Instances of all required objects. In addition, the SDK needs to

know how to reach the POS Service. For this purpose, a URL must be sent to the setup method. The

setup itself does not perform any request or checks whether the POS Service is available.

The SDK saves the Url automatically and uses it for all upcoming requests. It can be changed later on at

any time.

In addition to the URL, the SDK defines default values for the customers locale based on the mobile

device setting. Also this setting can be overwritten at any time within the shared instance of the main

class.

Method StartSelfscanningSession

The method startSelfscanningSession creates a session for the Selfscan process. The session is always

related to a shop (businessUnitId) and a customer. The SDK will return a status and a pos session

(SelfscanSDK class property), which will be automatically used for all upcoming requests to identify the

session at the POS Service.

SDK Methods

27

Platform  Method

Hint

iOS #1

+ (void) startSelfscanningSessionWithCustomerNumber:
(NSString *) customerNumber
                                     businessUnitId: (NSString *)
businessUnitId
                               autorizationCodeFlag: (BOOL)
autorizationCodeFlag
                                      completeBlock:
(SSCSelfscanSDKCompleteBlock_t) completeBlock;

iOS #2

+ (void) startSelfscanningSessionWithCustomerNumber:
(NSString *) customerNumber
                                     businessUnitId: (NSString *)
businessUnitId
                                      completeBlock:
(SSCSelfscanSDKCompleteBlock_t) completeBlock;

Android
#1

public static void startSelfscanningSession(String
customerNumber,
                                            String businessUnitId,
                                            Boolean authorizationCodeFlag,
                                            final
SSCSelfscanSDKCompleteCallback completeCallback)

Android
#2

public static void startSelfscanningSession(String
customerNumber,
                                            String businessUnitId,
                                            final
SSCSelfscanSDKCompleteCallback completeCallback)

The autorizationCodeFlag will be
automatically set to false when using this
method.

The autorizationCodeFlag will be
automatically set to false when using this
method.

Request parameters

Type

Description



customerNumber

String



businessUnitId

String

Opening a selfscanning session requires a known
customer. Use this parameter to send the card
number etc. of a customer to the POS Service to
start a selfscanning session. The parameter is
required and must not be null.

The businessUnitId identifies the shop of a
transaction. Each shop is linked to a locale,
masterdata, and so on. The parameter is required
and must not be null.



autorizationCodeFlag

Boolean

Not relevant - only used for specific projects. Send
false as default.



completeBlock /

completeCallback

SSCSelfscanSDKCompleteBlock_t
(iOS)

SSCSelfscanSDKCompleteCallback
(Android)

For all requests, a completion handler must be
specified. This one is triggered when the SDK
receives a response from the POS Service. The
completion handler contains an object of type
SelfscanSDKResponse which contains the
response parameters.

See response for more details.

 28

SDK Methods

Response parameters  Type

Description



operationStatus

SelfscanSDKOperationStatus / String  General status of the operation

  OK
  NOK



errorResponse

SSCErrorResponse

Details about an error in case something went wrong.

Method EndSelfscanningSession

The method endSelfscanningSession must be used to finish the Selfscan process. Calling this method

will send the transaction that is linked to the current session to the Backoffice server. An identification

number is returned that the transaction fetched by the cashier.

Platform  Method

iOS

+ (void) endSelfscanningSessionWithCompleteBlock: (SSCSelfscanSDKCompleteBlock_t) completeBlock;

Android  public static void endSelfscanningSession(final SSCSelfscanSDKCompleteCallback completeCallback)

Request parameters

Type

Description



completeBlock /

completeCallback

SSCSelfscanSDKCompleteBlock_t
(iOS)

SSCSelfscanSDKCompleteCallback
(Android)

For all requests, a completion handler must be
specified. This one is triggered when the SDK receives
a response from the POS Service. The completion
handler contains an object of type
SelfscanSDKResponse which contains the response
parameters.

See response for more details.

Response parameters  Type

Description



operationStatus

SelfscanSDKOperationStatus /
String

General status of the operation

  OK
  NOK



suspendNumber

String

Number to recover the transaction from Backoffice server by
the cashier.

  Note: The SDK will save the suspendNumber in the
SelfscanSDK class instance - it is not directly
returned in the response

SDK Methods

29

Response parameters  Type

Description



errorResponse

SSCErrorResponse

Details about the error in case something went wrong.

Method RegisterLineItem

A way to register new items is the method registerLineItem. The SDK provides three ways of this

method to simplify the requests. In case an item was added to the transaction with success, the

response contains all transaction items including the added one. Details about transaction and line

item properties can be found in one of the previous chapters.

Note: It is recommend using the processBarcode method instead. It will execute additional checks and

logic to analyze the barcode.

Platform  Method

Hint

iOS #1

+ (void) registerLineItemWithBarcode: (NSString *) barcode
                       quantityInput: (SWGQuantityInputSSC *)
quantityInput
                       completeBlock:
(SSCSelfscanSDKCompleteBlock_t) completeBlock;

iOS #2

+ (void) registerLineItemWithBarcode: (NSString *) barcode
                       completeBlock:
(SSCSelfscanSDKCompleteBlock_t) completeBlock;

The SWGQuantityInputSSC will be set
automatically by the SDK. The piece will be set to
1.

iOS #3

+ (void)
registerLineItemWithQuantityValidationAndBarcode:
(NSString *) barcode
                                            completeBlock:
(SSCSelfscanSDKCompleteBlock_t) completeBlock;

The SDK will automatically check whether the
item with the given barcode already exists within
the transaction. In case it does not exist, it will
add a new item with piece 1.

When the item already exists, it will increase the
quantity by 1.

Android
#1

Android
#2

public static void registerLineItem(String barcode,

                                    QuantityInputSSC quantityInputItem,
                                    final
SSCSelfscanSDKCompleteCallback completeCallback)

public static void registerLineItem(String barcode,

                                    final
SSCSelfscanSDKCompleteCallback completeCallback)

The QuantityInputSSC will be set automatically by
the SDK. The piece will be set to 1.

Android
#3

public static void
registerLineItemWithQuantityValidation(final String barcode,
                                                          final
SSCSelfscanSDKCompleteCallback completeCallback)

The SDK will automatically check whether the
item with the given barcode already exists within
the transaction. In case it does not exist, it will
add a new item with piece 1.

When the item already exists, it will increase the
quantity by 1.

 30

SDK Methods

Request parameters

Type

Description



barcode

String

Send the barcode (EAN, Code128, ...) of an item to the
SDK to register the item behind at the shopping cart.



quantityInput

(SWG)QuantityInputSSC



completeBlock /

completeCallback

SSCSelfscanSDKCompleteBlock_t
(iOS)

SSCSelfscanSDKCompleteCallback
(Android)

A complex type with quantity information. It can contain
length, pieces, and so on. For most items, only a piece
is relevant.

Hint: Use processBarcode to figure out which item
requires additional quantity information.

For all requests, a completion handler must be
specified. This one is triggered when the SDK receives
a response from the POS Service. The completion
handler contains an object of type
SelfscanSDKResponse which contains the response
parameters.

See response for more details.

Response parameters

Type

Description



operationStatus

SelfscanSDKOperationStatus / String  General status of the operation



registrationDetails

(SWG)RegistrationDetails

  OK
  NOK

Details about restrictions and quantity
inputs. In case some additional action like
entering quantities is necessary, the
operation status will be NOK.



transactionOperationResult

(SWG)TransactionOperationResultSSC SWGTransactionOperationResultSSC



errorResponse

SSCErrorResponse

Method ProcessBarcode

containing the full transactions and also
modified (added) line item.

Details about the error in case something
went wrong.

The method processBarcode analyzes items and adds them to the transaction afterwards. It is the

recommend way to do this. In case the item cannot be added (for example, due to some missing

information about dimension), the response will return this information and the item can be registered

afterwards using registerLineItem.

SDK Methods

Platform  Method

31

iOS

+ (void) processBarcodeWithBarcode: (NSString *) barcode
                       barcodeType: (SSCBarcodeType) barcodeType
                     completeBlock: (SSCSelfscanSDKCompleteBlock_t) completeBlock;

Android

processBarcode(SSCBarcodeType barcodeType,

                                  String barcode,
                                  final SSCSelfscanSDKCompleteCallback completeCallback)

Request parameters

Type

Description



barcode

String

Send the barcode (EAN, Code128, ...) of an item to the
SDK to get the item identified and added to the
shopping cart.



barcodeType

SSCBarcodeType

  UPCA(111)
  UPCE(112)
  EAN8(103)
  EAN13(104)
  CODE128(110)
  DATAMATRIX(203)
  QRCODE(204)



completeBlock /

completeCallback

SSCSelfscanSDKCompleteBlock_t
(iOS)

SSCSelfscanSDKCompleteCallback
(Android)

For all requests, a completion handler must be
specified. This handler is triggered when the SDK
receives a response from the POS service. The
completion handler contains an object of type
SelfscanSDKResponse which contains the response
parameters.

See response for more details.

Response parameters

Type

Description



operationStatus

SelfscanSDKOperationStatus / String  General status of the operation

  OK
  NOK



statusCode

String

Error or status code of the operation. See
table of error codes for more information.



registrationDetails

(SWG)RegistrationDetails

Details about restrictions and quantity
inputs. In case some additional action like
entering quantities is necessary, the
operation status will be NOK.

 32

SDK Methods

Response parameters

Type

Description



transactionOperationResult

(SWG)TransactionOperationResultSSC SWGTransactionOperationResultSSC



errorResponse

SSCErrorResponse

Method SetQuantity

containing the full transactions and also
modified (added) line item.

Details about the error in case something
went wrong.

The method setQuantity can be used to change the quantity of an item within the transaction.

Platform  Method

Description

iOS #1

iOS #2

+ (void) setQuantity: (SWGQuantityInputSSC *)
quantityInput
          ofLineItem:
(SWGRetailTransactionLineItemKeySSC *)
lineItemKey
       completeBlock:
(SSCSelfscanSDKCompleteBlock_t)
completeBlock;

+ (void) setPieces: (NSNumber *) pieces
        ofLineItem:
(SWGRetailTransactionLineItemKeySSC *)
lineItemKey
     completeBlock:
(SSCSelfscanSDKCompleteBlock_t)
completeBlock;

Method to set the quantity of an item. Depending on the
item type and item requirement, specific properties of the
quantity must be set (like length etc.).

To identify an item, see registrationDetails:
quantityInputMethod of registerLineItem or
processBarcode method response.

The method calls the setQuantity method by creating a
SWGQuantityInputSSC object with the given pieces
property.

Android
#1

public static void setQuantity(QuantityInputSSC
quantityInputItem,

Method to set the quantity of an item. Depending on the
item type and item requirement, specific properties of the
quantity must be set (like length etc).

RetailTransactionLineItemKeySSC lineItemKey,
                               final
SSCSelfscanSDKCompleteCallback
completeCallback)

To identify an item, see registrationDetails:
quantityInputMethod of registerLineItem or
processBarcode method response.

Android
#2

public static void setPieces(BigDecimal pieces,

RetailTransactionLineItemKeySSC lineItemKey,

The method calls the setQuantity method by creating a
SWGQuantityInputSSC object with the given pieces
property.

SSCSelfscanSDKCompleteCallback
completeCallback)

Request parameters

Type

Description



quantityInput

(SWG)QuantityInputSSC

The normal quantity object for any item which
contains



pieces

SDK Methods

33

Request parameters

Type

Description



pieces

NSNumber / BigDecimal



lineItemKey

(SWG)RetailTransactionLineItemKeySS
C



completeBlock /

SSCSelfscanSDKCompleteBlock_t (iOS)

completeCallbac
k

SSCSelfscanSDKCompleteCallback
(Android)


length
  width

height
  measure
  weight
  manualWeightInput


units

A simple parameter to describe the quantity of an
item by using pieces. Can be used for the most
items. The SDK will internally create a
QuantityInputSSC object and set the pieces
parameter.

The RetailTransactionLineItemKeySSC contains
information to identify an item within the transaction.
Normally, the RetailTransactionLineItemKeySSC
can be taken from any returned transaction - it is
part of SWGRetailTransactionLineItemSSC. Within
the RetailTransactionLineItemKeySSC, there are
three properties:






businessUnitGroupID

transactionID
retailTransactionLineItemSequenceNumbe
r

For all requests, a completion handler must be
specified. This handler is triggered when the SDK
receives a response from the POS Service. The
completion handler contains an object of type
SelfscanSDKResponse which contains the
response parameters.

See response for more details.

Response parameters

Type

Description



operationStatus

SelfscanSDKOperationStatus / String  General status of the operation

  OK
  NOK



statusCode

String

Error or status code of the operation. See
table of error codes for more information.



registrationDetails

(SWG)RegistrationDetails

Details about restrictions and quantity
inputs. In case some additional action like

 34

SDK Methods

Response parameters

Type

Description

entering quantities is necessary, the
operation status will be NOK.



transactionOperationResult

(SWG)TransactionOperationResultSSC SWGTransactionOperationResultSSC



errorResponse

SSCErrorResponse

Method VoidLineItem

containing the full transactions and also
modified line item.

Details about the error in case something
went wrong.

The method voidLineItem can be used to remove an item from the transaction. For this purpose, the

SDK needs to know which item should be removed. The item is identified by

SWGRetailTransactionLineItemKeySSC which is part of any line item of the transaction.

The item will be removed after calling the method independent on its quantity.

Platform  Method

iOS

+ (void) voidLineItem: (SWGRetailTransactionLineItemKeySSC *) lineItem
        completeBlock: (SSCSelfscanSDKCompleteBlock_t) completeBlock;

Android

public static void voidLineItem(RetailTransactionLineItemKeySSC lineItemKey,
                                final SSCSelfscanSDKCompleteCallback completeCallback)

Request parameters

Type

Description



lineItemKey

(SWG)RetailTransactionLineItemKeySS
C



completeBlock /

SSCSelfscanSDKCompleteBlock_t (iOS)

completeCallbac
k

SSCSelfscanSDKCompleteCallback
(Android)

The RetailTransactionLineItemKeySSC contains
information to identify an item within the transaction.
Normally, the RetailTransactionLineItemKeySSC
can be taken from any returned transaction - it is
part of SWGRetailTransactionLineItemSSC. Within
the RetailTransactionLineItemKeySSC, there are
three properties:





businessUnitGroupID
transactionID
retailTransactionLineItemSequenceNumbe
r

For all requests, a completion handler must be
specified. This handler is triggered when the SDK
receives a response from the POS Service. The
completion handler contains an object of type
SelfscanSDKResponse which contains the
response parameters.

See response for more details.

SDK Methods

35

Response parameters

Type

Description



operationStatus

SelfscanSDKOperationStatus / String  General status of the operation

  OK
  NOK



statusCode

String

Error or status code of the operation. See
table of error codes for more information.



registrationDetails

(SWG)RegistrationDetails

Details about restrictions and quantity
inputs. In case some additional action like
entering quantities is necessary, the
operation status will be NOK.



transactionOperationResult

(SWG)TransactionOperationResultSSC SWGTransactionOperationResultSSC



errorResponse

SSCErrorResponse

Method AnalyzeBarcode

containing the full transactions where the
removed item is no longer present.

Details about the error in case something
went wrong.

The analyzeBarcode method will perform a check of a barcode based on a given rule set. The rules

how a barcode is encoded might depend on the used POS Service. As a result, the POS Service will

return the type of the barcode.

Platform  Method

iOS

+ (void) analyzeBarcodeWithBarcode: (NSString *) barcode
                       barcodeType: (SSCBarcodeType) barcodeType
                     completeBlock: (SSCSelfscanSDKCompleteBlock_t) completeBlock;

Android

public static void analyzeBarcode(SSCBarcodeType barcodeType,

                                  String barcode,
                                  final SSCSelfscanSDKCompleteCallback completeCallback)

Request parameters

Type

Description



barcode

String

Send the barcode (EAN, Code128, ...) of an item to the
SDK to get the item identified.



barcodeType

SSCBarcodeType

  SSCBarcodeType_upca,
  SSCBarcodeType_upce,

 36

SDK Methods

Request parameters

Type

Description

  SSCBarcodeType_ean8,
  SSCBarcodeType_ean13,
  SSCBarcodeType_code128,
  SSCBarcodeType_dataMatrix,
  SSCBarcodeType_qrCode



completeBlock /

completeCallback

SSCSelfscanSDKCompleteBlock_t
(iOS)

SSCSelfscanSDKCompleteCallback
(Android)

For all requests, a completion handler must be
specified. This handler is triggered when the SDK
receives a response from the POS Service. The
completion handler contains an object of type
SelfscanSDKResponse which contains the response
parameters.

See response for more details.

Response parameters

Type

Description



operationStatus

SelfscanSDKOperationStatus /
String

General status of the operation

  OK
  NOK



statusCode

String

Error or status code of the operation. See table of
error codes for more information.



analyzeBarcodeResponse

(SWG)AnalyzeBarcodeResponse  Contains detailed information about the barcode

analysis, like line item operation.



"reactionName": "registerItem" >>
Normal item, which can be added to the
transaction

Method GetTransaction

The getTransaction method can be used to fetch the current status from the POS Service. Normally, the

POS Service will always return the latest status of the transaction after each line item operation, so

getTransaction does not have to be called separately.

Platform  Method

iOS

+ (void) getTransactionWithCompleteBlock: (SSCSelfscanSDKCompleteBlock_t) completeBlock;

Android

public static void getTransaction(final SSCSelfscanSDKCompleteCallback completeCallback)

SDK Methods

37

Request parameters

Type

Description



completeBlock /

completeCallback

SSCSelfscanSDKCompleteBlock_t
(iOS)

SSCSelfscanSDKCompleteCallback
(Android)

For all requests, a completion handler must be
specified. This handler is triggered when the SDK
receives a response from the POS Service. The
completion handler contains an object of type
SelfscanSDKResponse which contains the response
parameters.

See response for more details.

Response parameters

Type

Description



operationStatus

SelfscanSDKOperationStatus / String  General status of the operation

  OK
  NOK



statusCode

String

Error or status code of the operation. See
table of error codes for more information.



registrationDetails

(SWG)RegistrationDetails

Details about restrictions and quantity
inputs. In case some additional action like
entering quantities is necessary, the
operation status will be NOK.



transactionOperationResult

(SWG)TransactionOperationResultSSC SWGTransactionOperationResultSSC



errorResponse

SSCErrorResponse

Method CreateTransaction

containing the full transactions and also
modified (added) line items. Since
getTransaction does no item operations, no
added or modified items will be returned.

Details about the error in case something
went wrong.

The method createTransaction will manually create a new transaction in case this is not done yet.

Normally, it is not necessary to call this method because the POS Service will automatically create a

new transaction when registerLineItem or processBarcode is called and this is not done yet.

Platform  Method

iOS

+ (void) createTransactionWithCompleteBlock: (SSCSelfscanSDKCompleteBlock_t) completeBlock;

Android

public static void createTransaction(final SSCSelfscanSDKCompleteCallback completeCallback)

 38

SDK Methods

Request parameters

Type

Description



completeBlock /

completeCallback

SSCSelfscanSDKCompleteBlock_t
(iOS)

SSCSelfscanSDKCompleteCallback
(Android)

For all requests, a completion handler must be
specified. This handler is triggered when the SDK
receives a response from the POS Service. The
completion handler contains an object of type
SelfscanSDKResponse which contains the response
parameters.

See response for more details.

Response parameters

Type

Description



operationStatus

SelfscanSDKOperationStatus / String  General status of the operation

  OK
  NOK



statusCode

String

Error or status code of the operation. See
table of error codes for more information.



transactionOperationResult

(SWG)TransactionOperationResultSSC SWGTransactionOperationResultSSC



errorResponse

SSCErrorResponse

Method CancelTransaction

containing the empty transaction with some
information

Details about the error in case something
went wrong.

The method cancelTransaction will cancel the current transaction. It can be recovered afterwards by

calling recoverTransaction.

Platform  Method

iOS

+ (void) cancelTransactionWithCompleteBlock: (SSCSelfscanSDKCompleteBlock_t) completeBlock;

Android

public static void cancelTransaction(final SSCSelfscanSDKCompleteCallback completeCallback)

Request parameters

Type

Description



completeBlock /

completeCallback

SSCSelfscanSDKCompleteBlock_t
(iOS)

SSCSelfscanSDKCompleteCallback
(Android)

For all requests, a completion handler must be
specified. This handler is triggered when the SDK
receives a response from the POS Service. The
completion handler contains an object of type
SelfscanSDKResponse which contains the response
parameters.

SDK Methods

39

Request parameters

Type

Description

See response for more details.

Response parameters

Type

Description



operationStatus

SelfscanSDKOperationStatus / String

General status of the operation

  OK
  NOK

Method RecoverTransaction

To restore an old transaction, the recoverTransaction should be used. Cases for such transaction can be

that it was canceled or the session was ended by saving the transaction to the Backoffice server. The

recoverTransaction requires a selfscanning session which is created automatically by the SDK with the

given properties.

Platform  Method

iOS

+ (void) recoverTransactionWithCompleteBlock: (SSCSelfscanSDKCompleteBlock_t) completeBlock;

Android  public static void recoverTransaction(final SSCSelfscanSDKCompleteCallback completeCallback)

Request parameters

Type

Description



completeBlock /

completeCallback

SSCSelfscanSDKCompleteBlock_t
(iOS)

SSCSelfscanSDKCompleteCallback
(Android)

For all requests, a completion handler must be
specified. This handler is triggered when the SDK
receives a response from the POS Service. The
completion handler contains an object of type
SelfscanSDKResponse which contains the response
parameters are within.

See response for more details.

Response parameters

Type

Description



operationStatus

SelfscanSDKOperationStatus / String  General status of the operation

  OK
  NOK



statusCode

String

Error or status code of the operation. See
table of error codes for more information.

 40

SDK Methods

Response parameters

Type

Description



registrationDetails

(SWG)RegistrationDetails

Details about restrictions and quantity
inputs. In case some additional action like
entering quantities is necessary, the
operation status will be NOK.



transactionOperationResult

(SWG)TransactionOperationResultSSC SWGTransactionOperationResultSSC



errorResponse

SSCErrorResponse

containing the full recovered transaction of
the given user / businessUnit.

Details about the error in case something
went wrong.

41

Error Codes

Error Codes

Code-ID

Message

GKR-00000

Unknown runtime error

GKR-00001

Invalid session

GKR-00003

Characters entered are not valid!

GKR-00005

An unexpected application error occurred. Please try the operation again. If the problem happens
again, please contact support.

GKR-00006

Not allowed argument for internal function call occurred!

GKR-00007

The error does not contain any error information!

GKR-00008

The error does not contain an error code!

GKR-00500

Service cannot be reached!

GKR-00900

Check digit is not correct!

GKR-00901

Verification of check digit failed - method not supported.

GKR-00902

Input is too short!

GKR-00903

Input is too long!

GKR-00904

Invalid amount!

GKR-10000

Authentication failed. Invalid user or password.<br/>Please try again.

GKR-10001

Invalid password!

GKR-10002

Training mode not allowed!

GKR-10010

Operation failed. The user session is locked.

GKR-10011

Cashier {0} not allowed to finish lock!

GKR-10020

Logout not possible!

GKR-10021

Cashier {0} not allowed to log out!

GKR-10030

Drawer not assigned.

GKR-10031

Please enter login!

 42

Error Codes

Code-ID

Message

GKR-10032

Till Copy Object not available!

GKR-10041

Cashier already logged in at the cash register {0}.

GKR-10043

Operator {0} doesn't have permission to sign on the drawer {1}.

GKR-10044

Drawer already signed on another cash register.

GKR-10045

Workstation {0} doesn't have permission to sign on the drawer {1}.

GKR-10046

Workstation {0} is already registered on different address.

GKR-10047

Safe {0} is currently locked.

GKR-10050

No authority to perform this function!

GKR-10051

Second cashier or manager authorization required!

GKR-10100

Transaction is not valid!

GKR-20000

Printout is not possible!

GKR-20001

Printer cover open!

GKR-20002

Printer is out of paper!

GKR-20003

Printer not reachable - check connection!

GKR-20020

Terminal sign on failed.

GKR-20021

Terminal sign off failed.

GKR-20022

Payment failed due to terminal error!

GKR-20023

Function not possible!<br>POS-Service not available.

GKR-20026

Input is too short!

GKR-20027

Input is too long!

GKR-20028

<html>Payment not possible!<br>Terminal not available!

GKR-20029

<html>Refund not possible!<br>Refund only possible from {0} until {1}!

GKR-20030

<html>Refund not possible!<br>Maximum refund amount {0} {1} exceeded!

GKR-21000

GKR-21001

Common scale error!

Error Codes

43

Code-ID

Message

GKR-21002

Internal Scale Error 1

GKR-21003

Internal Scale Error 2

GKR-21004

Internal Scale Error 3

GKR-21005

Internal Scale Error 4

GKR-21006

Internal Scale Error 5

GKR-21007

Scale swings too long!

GKR-21008

Please put weight again!

GKR-21009

Scale swings too long!

GKR-21010

No weight on the scale!

GKR-21011

Weight is too small!

GKR-21012

Weight is too heavy!

GKR-21013

Internal Scale Error 6

GKR-21014

Internal Scale Error 7

GKR-21015

Internal Scale Error 8

GKR-21016

Internal Scale Error 9

GKR-21017

Internal Scale Error 10

GKR-21018

Printer is not ready!

GKR-21019

Please put weight on scale!

GKR-21020

Weighing in progress, please wait ...

GKR-21021

Weight successfully determined!

GKR-21022

Sum Module could not be validated!

GKR-21023

Total price too small!

GKR-21024

Total price too high!

GKR-21025

Weight process cancelled. Incompatible settings for weight units for scale and POS!

GKR-21026

Scale is outside of zero capture range!

Error Codes

 44

Code-ID

Message

GKR-21027

Checking of scale print layout failed due to missing mandatory fields!

GKR-22000

Unspecified hardware management error!

GKR-22001

The device {0} has been already activated!

GKR-22002

The device {0} is not inactive!

GKR-22003

The device {0} was not opened correctly!

GKR-22004

Error occurred while firing device activation event for device {0}!

GKR-23001

Fiscal printout not possible

GKR-23002

Limit of reprint attempts reached

GKR-23003

The fiscal printer recovery failed (state={0})!

GKR-30001

Coupon cannot be used!

GKR-30010

Discount not possible!

GKR-30011

Line item discount not permitted!

GKR-30012

Item cannot be discounted!

GKR-30013

Item price must be greater than 0!

GKR-30014

Price entry not allowed for this line item!

GKR-30015

Price increase not permitted!

GKR-30016

Price reduction not permitted!

GKR-30017

Maximum number of discounts have been applied!

GKR-30018

Item missing!

GKR-30019

Maximum quantity {0} exceeded!

GKR-30020

Condition value is missing!

GKR-30021

Required condition has not been satisfied!

GKR-30022

Transaction discount not allowed!

GKR-30023

Configuration error!

GKR-30024

Maximum number of discounts have been applied!

Error Codes

45

Code-ID

Message

GKR-30025

Discount not possible. Campaign is missing!

GKR-30026

Limit exceeded!

GKR-30040

Receipt cannot be suspended!

GKR-30050

Suspended receipt cannot be retrieved!

GKR-30051

Impossible to retrieve scale receipt!

GKR-30052

<html>Configuration error!<br/>Item is missing!

GKR-30053

Empties return not possible!

GKR-30054

<html>Configuration error!<br/>Item is missing!

GKR-30060

No valid tax rate exists!<br>Entry not possible!

GKR-30100

Function not possible!

GKR-70040

Configuration not found!

GKR-70041

Invalid configuration.

GKR-75000

Invalid GTIN barcode.

GKR-75001

Check digit not correct!

GKR-87000

No item was found!

GKR-87001

More than {0} items have been found.<br/>Only {0} items can be displayed.<br/>Refine your search
criteria or press Continue.

GKR-88000

The request process definition could not be found

GKR-88001

The request process definition is not valid

GKR-88002

The preconditions to start a process or run a step are not fulfilled

GKR-88003

The process execution failed for some internal error!<br/> Please contact Support!

GKR-88004

Function not possible!

GKR-89000

Screen layout does not exist.

GKR-89001

The screen layout validation or rendering failed.

GKR-89002

The screen hiding failed.

 46

Error Codes

Code-ID

Message

GKR-89003

The screen reloading failed.

GKR-90010

Business unit group does not exist.

GKR-90015

Business unit group item does not exist.

GKR-90020

Business unit does not exist.

GKR-90025

Pos identity does not exist!

GKR-90029

Pos identity is locked

GKR-90040

Currency does not exist!

GKR-90045

No such tender. Tender does not exist!

GKR-90055

Item selling price does not exist!

GKR-90056

{0} is an unknown salesperson number!

GKR-90060

Cashier does not exist!

GKR-90061

Error occurred - operator not saved!

GKR-90062

Error occurred - operator not deleted!

GKR-90070

Merchandise category does not exist!

GKR-90071

Merchandise category tender permission does not exist!

GKR-90075

Item {0} not found!

GKR-90080

Employee number not found!

GKR-90383

Employee is not eligible for discounts!

GKR-90384

Employee is logged in as cashier. Employee purchase not allowed!

GKR-90385

Employee number is not found!

GKR-90386

Employee purchase not allowed!

GKR-90432

No item was found!

GKR-90090

Exchange rate does not exist!

GKR-90095

Workstation does not exist!

GKR-90135

Promotion not applicable - price is already changed.

Error Codes

Code-ID

Message

47

GKR-90136

Promotion not applicable - prices of all sales line items are manually changed.

GKR-90137

Promotion not applicable - limit exceeded.

GKR-90138

Promotion not applicable on return!

GKR-90140

Receipt {0} not reprintable!

GKR-90141

Reprint of receipt {0} not allowed!

GKR-90142

Original receipt was changed. Printing not possible!

GKR-90151

Offline! Invoice printing not possible!

GKR-90152

Function not possible!

GKR-90153

Invoice printing not allowed for this document type!

GKR-90204

<html>No valid tax rate exists!<br> Entry not possible!

GKR-90209

Could not calculate tax!

GKR-90221

Tender pickup not possible in current cash register mode!

GKR-90222

Loan/Change is not possible!

GKR-90223

Tender pickup required!

GKR-90226

Customer tender does not exist.

GKR-90229

Receipt cannot be canceled!

GKR-90230

No such tender adjustment rule!

GKR-90231

No such tender sale return rule!

GKR-90301

The login {0} does not exist!

GKR-90302

Login {0} is invalid!

GKR-90303

Login {0} is locked!

GKR-90304

The password for login {0} has expired!

GKR-90305

The password is too long!

GKR-90306

The password is too short!

GKR-90307

The password contains too few letters!

 48

Error Codes

Code-ID

Message

GKR-90308

The password contains too many letters!

GKR-90309

The password contains too few numbers!

GKR-90310

The password contains too many numbers!

GKR-90311

The password contains too few special characters!

GKR-90312

The password contains too many special characters!

GKR-90313

The entered password was already used!

GKR-90314

The password is empty!

GKR-90401

The drawer's receipts are currently being processed.

GKR-90402

Document flow not finished.

GKR-90403

You are not authorized for this drawer.

GKR-90404

There are unprocessed receipts for this drawer.

GKR-90405

The selected drawer is a training drawer!

GKR-90406

Cashier already logged in at the cash register {Cash register number of the other cash register}

GKR-90407

Accounts are in progress. Please wait ...

GKR-90408

Accounts results unknown due to offline! Please check the drawer status!

GKR-90409

Internal error! Accounts could not be completed!

GKR-90410

Receipt processing is not completed yet!

GKR-90411

No drawer found!

GKR-90412

Offline! Accounts not possible!

GKR-90413

Accounts not possible!

GKR-90430

No packagings available!

GKR-90431

The item {0} was not found!

GKR-90433

Packaging selection not possible!

GKR-99000

Receipt not found.

GKR-99001

Could not store receipt.

Error Codes

49

Code-ID

Message

GKR-99002

Receipt not deleted!

GKR-99003

Impossible to save scoped transactions!

GKR-99004

Receipt has no items!

GKR-99005

No suspended receipt available

GKR-99023

No receipts found!

GKR-99024

No receipt found!

GKR-99006

Transaction extensions cannot be copied.

GKR-99009

Receipt found {1} does not correspond to receipt expected {1}!

GKR-99010

Line item not found!

GKR-99011

Could not save line item

GKR-99012

Could not create line item

GKR-99013

Line item must be finished in order to proceed!

GKR-99014

The item {0}, {1} is blocked for sale!

GKR-99015

Subtotal not possible.

GKR-99016

Server not available!

GKR-99018

Could not store receipt

GKR-99030

Maximum line item limit exceeded!

GKR-99031

Limit exceeded!

GKR-99032

Maximum price difference exceeded!

GKR-99033

Repetition not allowed!

GKR-99034

Maximum quantity exceeded!

GKR-99035

Minimum quantity required not met!

GKR-99036

Quantity entry not allowed!

GKR-99037

Quantity requirement has not been met!

GKR-99038

Single quantity input isn't allowed.

 50

Error Codes

Code-ID

Message

GKR-99039

No weighing result available!

GKR-99040

Quantity entered not allowed!

GKR-99041

Quantity missing!

GKR-99042

Quantity must be an integer!

GKR-99043

Minimum quantity {0} has not been met!

GKR-99044

Maximum quantity {0} exceeded!

GKR-99045

Maximum allowed quantity {0} for line item discounts exceeded!

GKR-99046

Line item total minimum of {0} has not been met by {1}!

GKR-99047

Limit exceeded!

GKR-99048

Single quantity input is not allowed for this item.

GKR-99049

Wrong entry!

GKR-99050

Tender is not valid for this transaction!

GKR-99051

Invalid amount!

GKR-99052

The maximum amount for this tender is {0}!

GKR-99053

The minimum amount for this tender is {0}!

GKR-99054

Tender is not permitted!

GKR-99055

Tender is not permitted!

GKR-99056

Tender is not allowed for this customer!

GKR-99057

Transaction restricted to a one tender type!

GKR-99058

Tender is not allowed for return!

GKR-99059

Tender is not allowed for sale!

GKR-99060

Tender is not permitted for this receipt!

GKR-99061

Tender is not allowed for existing line items!

GKR-99062

Tender is not allowed for this customer group!

GKR-99063

Tender is not allowed for all customer!

Error Codes

51

Code-ID

Message

GKR-99064

Tender is not permitted for this receipt!

GKR-99065

Tender is not allowed for pay-in!

GKR-99066

Tender is not allowed for pay-in reason!

GKR-99067

Tender is not allowed for pay-out reason!

GKR-99068

Payment exceeds total due!

GKR-99069

Payment is less than minimum due!

GKR-99070

Tender cannot be combined with other tenders!

GKR-99071

Tender is only allowed virtual in training mode!

GKR-99076

Price of 0.00 is inadmissible!

GKR-99079

Price change is not permitted!

GKR-99080

Price change to 0.00 not allowed!

GKR-99090

Limit exceeded!

GKR-99091

Limit exceeded!

GKR-99092

Pay-in not possible!

GKR-99093

Pay-out not possible!

GKR-99100

Receipt has already been returned!

GKR-99101

Receipt has already been voided!

GKR-99102

Receipt not canceled!

GKR-99103

Line item already canceled.

GKR-99104

Canceling line item is not permitted!

GKR-99105

Line item is already completely returned.

GKR-99106

Line item cannot be returned.

GKR-99107

Receipt has no items to return!

GKR-99108

The line item cannot be modified.

GKR-99109

Line item must be finished in order to proceed!

 52

Error Codes

Code-ID

Message

GKR-99110

Receipt not closed!

GKR-99111

Last line item cannot be canceled!

GKR-99112

The item {0}, {1} is blocked for return!

GKR-99113

<html>Function not possible!<br> Line item must be finished in order to proceed!

GKR-99114

Tender {0} cannot be canceled.

GKR-99115

Receipt not suspended!

GKR-99116

Prepaid line item cannot be selected!

GKR-99117

Function impossible. There are open line items!

GKR-99120

Document {0} is not a sales receipt!

GKR-99121

Invalid currency!

GKR-99122

This receipt has already been returned in the current receipt!

GKR-99123

Receipt was already completely returned!

GKR-99124

Line item cannot be marked.

GKR-99125

Receipt from other store not allowed!

GKR-99150

Line item already voided!

GKR-99151

Function not allowed for this return line item!

GKR-99152

Function not allowed for this line item!

GKR-99153

Function not allowed for this line item in the current POS mode!

GKR-99200

Invalid drawer number!

GKR-99250

<html>Complete return not possible! <br/>Document contains prepaid line items.

GKR-99251

An error occurred while retrieving the prepaid PINs!

GKR-99252

<html>Transaction number is not unique.<br/>{0}

GKR-99253

<html>Internal problem.<br/>{0}

GKR-99254

<html>No connection.<br/>{0}

GKR-99255

<html>Internal problem.<br/>{0}

Error Codes

53

Code-ID

Message

GKR-99256

<html>Prepaid item is unknown.<br/>{0}

GKR-99257

<html>Not enough PIN codes.<br/>{0}

GKR-99258

Returning of prepaid items is not allowed!

GKR-99259

Quantity entry not allowed!

GKR-99260

Quantity is not an integer!

GKR-
01070100202.01

GKR-
01070100203.01

GKR-
01070100908.01

<html>{0}<br>Sale impossible!

<html>{0}<br>Return impossible!

<html>{0}<br>Redemption impossible!

GKR-99300

Maximum number of gift certificates exceeded!

GKR-99301

{0} {1} already used!

GKR-99302

Item {0} not found!

GKR-99303

The amount {0} is over the allowable limit {1}!

GKR-99304

The amount {0} is under the allowable minimum!

GKR-99305

The amount {0} does not match required denomination!

GKR-99350

Function not allowed in current POS mode!

GKR-99351

Line item still open!

GKR-99352

Value of gift card is 0!

GKR-99360

Invalid amount!

GKR-99361

Value of gift card is 0!

GKR-99362

Invalid count!

GKR-99363

{0} {1} has already been redeemed!

GKR-99364

Maximum amount {0} exceeded!

GKR-99401

Problem with Stored Value Server!

GKR-99402

Card is new - Not yet activated!

Error Codes

 54

Code-ID

Message

GKR-99403

Card no longer valid

GKR-99404

Card is blocked!

GKR-99405

No adequate credit available

GKR-99406

Card not authorized

GKR-99407

Wrong top-up amount for current card

GKR-99408

The amount is over the allowable limit!

GKR-99409

Reloading of gift card is not allowed!

GKR-99410

System error: user not authorized for this function!

GKR-99411

System error: error in loading the gift certificate range

GKR-99412

Unknown card

GKR-99413

System error: unknown company

GKR-99414

Card is new - Not yet activated!

GKR-99415

System error: authentication failed

GKR-99416

System error: connection to Stored Value Server failed.

GKR-99417

Posting failed.<br/>Please repeat.

GKR-99418

Problem with Stored Value Server!

GKR-99419

System error: operation not permissible

GKR-99420

Amount not permissible

GKR-99421

System error: currency tendered does not match gift card currency!

GKR-99422

Item cannot be voided!

GKR-99423

Gift certificate is not a valid!

GKR-99424

System error: transaction number invalid

GKR-99425

System error: country code invalid

GKR-99426

System error: store number invalid

GKR-99427

System error: cash register number invalid

Error Codes

55

Code-ID

Message

GKR-99428

System error: time stamp invalid

GKR-99429

System error: receipt data entered is not valid!

GKR-99430

System error: cancelation transaction number invalid

GKR-99431

Gift certificate type is not valid!

GKR-99432

System error: validity period incorrect

GKR-99433

Gift certificate not found!

GKR-99434

Gift certificate has already been redeemed.

GKR-99435

Gift certificate sale not allowed!

GKR-99436

Stored Value Server cannot be reached!

GKR-99500

Entry not allowed!

GKR-99501

Quantity restriction on item has been exceeded!

GKR-99502

<html>Maximum sales quantity of the item is {0}.<br>Entry not allowed!

GKR-99503

No empties!

GKR-99600

Customer {0} not found!

GKR-99601

Customer already exists!

GKR-99602

Customer cannot be added after tender!

GKR-99603

Customer cannot be added after tender!

GKR-99604

Customer cannot be added after tender!

GKR-99605

Web service is not suitable for card number search!

GKR-99606

Customer data entry not possible!

GKR-99700

No tax available!

GKR-99701

The tax amount must be between {0} and {1}!

GKR-99702

The tax rate must be between {0}% and {1}%!

GKR-99800

Tax exemption is not allowed for this item!

GKR-99850

Tax rate has not been defined.

 56

Error Codes

Code-ID

Message

GKR-99900

No points account available!

GKR-99901

Points balance not available!

GKR-99902

No points available!

GKR-99903

{0}<br>Redemption of points not possible!

GKR-99904

Customer data not available!

GKR-
01050101107.01

GKR-
01050101107.02

GKR-
01000101406.01

GKR-
01000101406.02

GKR-
01180101475.01

GKR-
01180101475.02

GKR-
01180101410.01

GKR-
01180101410.02

GKR-
01180101474.01

GKR-
01180101474.02

GKR-
01180101422.01

GKR-
01180101422.02

GKR-
01180101411.01

GKR-
01180101411.02

Impossible to cancel customer card!

No customer card available!

<html>Terminal error<br>Terminal EndOfDay failed!

<html>Terminal error<br>Terminal EndOfDay failed!<br>Code {0}: {1}

<html>Terminal error<br>Terminal key exchange failed!

<html>Terminal error<br>Terminal key exchange failed!<br>Code {0}: {1}

<html>Terminal error<br>Terminal init failed!

<html>Terminal error<br>Terminal init failed!<br>Code {0}: {1}

<html>Terminal error<br>Terminal EMV data print-out failed!

<html>Terminal error<br>Terminal EMV data print-out failed!<br>Code {0}: {1}

<html>Terminal error<br>Terminal Restart failed!

<html>Terminal error<br>Terminal-Restart failed!<br>Code {0}: {1}

<html>Terminal error<br>Network Diagnostic failed!

<html>Terminal error<br>Network Diagnostic failed!<br>Code {0}: {1}

Error Codes

Code-ID

Message

57

GKR-
01180101417.01

GKR-
01180101417.02

GKR-
01180100902.01

GKR-
01040100604.01

GKR-
01040100604.02

GKR-
01040100604.03

GKR-
01040100604.04

GKR-
01040100604.05

GKR-
01040100604.06

GKR-
01040100604.07

GKR-
01040100604.08

GKR-
01040100604.09

GKR-
01040100604.10

GKR-
01040100604.11

GKR-
01040100604.12

GKR-
01040100604.13

<html>Terminal error<br>Terminal Reprint failed!

<html>Terminal error<br>Terminal Reprint failed!<br>Code {0}: {1}

Terminal payment not possible!

Receipt not available due to offline!

Void receipt not possible!

Invalid receipt date! Receipt is not voidable.

Receipt contains non-voidable line items!<br />Receipt cannot be voided.

{0}<br />Tender {1} is not voidable!

Receipt already voided!

Internal error!<br />Receipt is not voidable.

A canceled receipt is not voidable!

{0}<br />Receipt is not voidable.

Receipt contains non-voidable tenders!<br />Receipt cannot be voided.

Terminal payment is not voidable!

Receipt cannot be voided on this cash register!

Void receipt not allowed for this receipt!

GKR-101014

Line item already canceled!

GKR-101015

Line item is not a gift certificate.

 58

Error Codes

Code-ID

Message

GKR-101016

Line item are not bonus points.

GKR-101017

Line item is not a card payment.

GKR-101021

Tender line item not specified.

GKR-101022

Tender line item is already canceled.

GKR-101023

Tender line item itself is to be canceled.

GKR-101101

{0}<br />Tender {1} is not voidable!

GKR-101103

{0}<br>Tender {1} cannot be canceled!

GKR-101104

No tender line item exists!

GKR-102000

This receipt can not be sent via e-mail!

GKR-102001

E-mail address is invalid!

GKR-102002

Function not possible!

GKR-102003

This receipt can not be sent via e-mail!

GKR-100000

<html>Web service initialized with wrong stub class.

GKR-100005

<html>Could not connect to server.

GKR-100006

<html>Query was not successful!<br>{0}

GKR-100010

<html>Cannot access Web Server!

GKR-100015

<html>Customer order {0} not found!

GKR-100020

Customer {0} not found!

GKR-100021

<html>{0}<br>Customer data not available!

GKR-100025

<html>A problem occurred during the request.

GKR-100027

<html>Line item must be finished in order to proceed!<br>Function not possible!

GKR-100030

Customer order not extendable!

GKR-100031

<html>Customer order does not exist!<br>{0}</html>

GKR-100035

<html>{0}<br>Validation not possible!

GKR-100040

<html>{0}<br>Booking not possible!

Error Codes

59

Code-ID

Message

GKR-100201

{0}<br>Gift certificate cannot be canceled!

GKR-100301

Service does not respond!

GKR-100401

Internal error

GKR-100402

Could not connect to server!

GKR-100403

Receipt already redeemed!

GKR-100404

Receipt voided!

GKR-100405

Receipt does not exist!

GKR-100406

Receipt already cleared!

GKR-100407

Invalid external transaction data!

GKR-100601

Function not possible!

GKR-100602

Configuration error!

GKR-100603

Wrong amount!

GKR-100701

valuephone customer already exists!

GKR-100702

<html>{0}<br/>valuephone transaction not possible!!

GKR-100703

<html>{0}<br/>valuephone payment not possible!!

GKR-100705

Currency invalid!

GKR-100801

Stock data could not be retrieved!

GKR-100802

Webshop item data could not be retrieved!

GKR-200001

Fiscal validation of transaction's tenders failed!<br/>{0}

GKR-200002

Fiscal validation of transaction's sub-total failed!<br/>{0}

GKR-200003

Fiscal validation of transaction positions failed!<br/>{0}

GKR-200101

End of day amount limit of {0} must not be exceeded by {1}!

GKR-200102

Amount for payment position too high!

GKR-200103

Position amount limit of {0} must not be exceeded by {1}!

GKR-200104

Position quantity of {0} must not exceed quantity limit of {1}!

 60

Error Codes

Code-ID

Message

GKR-200105

The tax group {0} of line item {1} is invalid!

GKR-200106

Price 0.00 for line item {0} is not allowed!

GKR-200107

{0} exceeds number of allowed positions of {1}!

GKR-200109

No receipt was submitted for checking!

GKR-200110

Return line items are not allowed for this receipt!

GKR-200111

The total {0} of tax rate {1} must not be smaller than 0.00 !

GKR-200112

Count of tender groups {0} must not exceed limit of {1}!

GKR-200113

Count of tenders {0} must not exceed limit of {1}!

GKR-200114

Receipt total amount is too high!

GKR-200115

Payment amount {0} is negative!

GKR-200116

Fiscal reserved word '{0}' present in article description of position {1}!

GKR-200117

Tender is not permitted: {1}!

GKR-200119

Position text contains forbidden characters!

GKR-200201

Price limit of {0} exceeded.

GKR-200400

Fiscalization related error has occurred<br>{0}

GKR-200401

Fiscal printer does not belong to this POS!<br>Please call the service for pairing!

GKR-200402

The EJ medium not present!

GKR-200403

The EJ medium is full!

GKR-200404

The EJ medium is near full!

GKR-200405

Error getting EJ medium status: code={0}!

GKR-200406

Fiscal printer not ready!

GKR-200407

Fiscal printer not assigned!<br>{0}

GKR-200408

EJ initialization could not be performed!

GKR-200409

Report printing could not be performed!

GKR-200500

Registration of item not allowed

Error Codes

61

Code-ID

Message

GKR-200501

Transaction (item) already redeemed

GKR-200502

No amount for transaction scale

GKR-200503

Unknown action

GKR-200504

Sale of gift certificate is not allowed

GKR-200505

Registration of item not possible

Any other code

Contact the GK support

List of abbreviations

 62

List of abbreviations

Abbreviation Meaning

POS

Point of Sale

BYOD

Bring your own device - customers can scan item barcodes using their own Smartphone with Android or
iOS

Contact

GK SOFTWARE SE

Waldstraße 7

08261 Schöneck

Germany

Tel.:  +49 (0) 3 74 64 84 – 0

Fax :  +49 (0) 3 74 64 84 - 15

E-mail: documentation@gk-software.com

www.gk-software.com

