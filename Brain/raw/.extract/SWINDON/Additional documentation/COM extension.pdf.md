BroadVision One-To-One Enterprise

COM Extension

1

To access a COM object from a BroadVision page script, you create an ActiveXObject object that is
bound to the COM object, and then access the properties and methods of the COM object by calling
the function or referencing the attributes of the ActiveXObject object. For example, a call to the
Work() method of a COM object called Sleep.Sleeper:

BroadVision® One-To-One™ Enterprise provides components for accessing Component Object
Model (COM) objects in the Microsoft Windows NT environment. The components, ActiveXObject
and Enumerator, are modeled after Microsoft’s JScript ActiveXObject and Enumerator COM
objects. This close modeling provides a high degree of compatibility between the Microsoft JScript
environment — typically used in Active Server Pages (ASP) — and the BroadVision page script
environment.

DRAFT

// Call a function of the COM object.
sleeper.Work(10);
%>

<%
// Instantiate a One-To-One object that references a COM object.
var sleeper = new ActiveXObject("Sleep.Sleeper");

l “ActiveXObject” on page 6. This component provides access to the COM objects.

l “Using the COM extension,” described next

This document provides information about

l “Enumerator” on page 8. This component provides access a COM collection.

You can also run samples that demonstrate various ways of using COM object in page scripts. The
samples are installed in the $BV1TO1\samples\activex directory on Windows NT installations
of BroadVision® One-To-One™ Enterprise.

One-To-One COM Extension

BroadVision, Inc.

2

BroadVision One-To-One Enterprise COM Extension
Using the COM extension

Using the COM extension

To use the COM extension, you will ﬁrst need to conﬁgure One-To-One and the Interaction Manager
servers to support this feature. The instructions for doing so are described in “Conﬁguring
One-To-One for the COM extension,” next.

The rest of this section describes:

l “Accessing COM object properties” on page 2, and

l “Accessing COM object functions” on page 4.

For detailed information about the COM extension objects, see “ActiveXObject” on page 6, and
“Enumerator” on page 8.

Conﬁguring One-To-One for the COM extension

After the COM extension is installed on your system, you need to conﬁgure One-To-One to use it. To
do that:

1. Edit your $BV1TO1_VAR\etc\bv1to1.conf conﬁguration ﬁle and add this line to the Export

section of the ﬁle:

BV_ENABLE_COM=1

2. Shutdown the Interaction Manager and One-To-One servers, and execute the changes.

imgr_conf -a stop
bvconf shutdown
bvconf execute -a install_all
imgr_conf -a start

You can now use the COM extension.

Accessing COM object properties

The ActiveXObject component provides get and set access to the properties of the contained COM
object. To access these properties through the ActiveXObject component, reference them as
demonstrated in this example:

var sample = new ActiveXObject("ISample");
sample.aProperty;
var i = sample.aProperty = 1;
var j = sample.Item(0);

// Get a property
// Set a property
// Get an indexed property

You cannot perform a set operation on an indexed property item; that operation is not supported.
Most objects supply an alternative method with similar semantics so that no functionality is lost
when COM objects are used in JavaScript.

BroadVision, Inc.

One-To-One COM Extension

Mappings

This table describes the mappings between COM data types and the corresponding BVI_Value data
type:

BroadVision One-To-One Enterprise COM Extension
Using the COM extension

3

COM Variant

Mapping

BVI_Value

VT_ARRAY —X—

—

VT_BOOL

VT_BSTR

VT_BSTR

<— —>
<— (1)
<— (1)

BVC_BOOLEAN_TYPE

BVC_DICT_TYPE

BVC_ENUM_TYPE

VT_BSTR

<— —>

BVC_STRING_TYPE

VT_DATE

VT_DISPATCH

—>

—>

BVI_DateTime

ActiveXObject

VT_EMPTY

<— —>

BVC_NULL_TYPE

VT_EMPTY

<— —>

BVC_UNKNOWN_TYPE

VT_ERROR —X—

—

VT_I1

<— —>

BVC_CHAR_TYPE

VT_I2

<— —>

BVC_SHORT_TYPE

VT_I4

<— —>

BVC_INT_TYPE

VT_I4

<— —>

BVC_LONG_TYPE

VT_R4

<— —>

BVC_FLOAT_TYPE

VT_R8

<— —>

BVC_DOUBLE_TYPE

VT_UI1

<— —>

BVC_OCTET_TYPE

VT_UI1

<— —>

BVC_UCHAR_TYPE

VT_UI2

<— —>

BVC_UINT_TYPE

VT_UI2

<— —>

BVC_USHORT_TYPE

VT_UI4

<— —>

BVC_ULONG_TYPE

VT_UNKNOWN —X—

—

All other values, attempt to
convert to string (VT_BSTR)

—>

BVC_STRING_TYPE

(1) If the typename property is “ActivexObject” then convert to VT_DISPATCH; if the typename property
is “BVI_DateTme”, convert to VT_DATE; everything else attempt to convert to string (VT_BSTR).

One-To-One COM Extension

BroadVision, Inc.

4

BroadVision One-To-One Enterprise COM Extension
Using the COM extension

Accessing COM object functions

The ActiveXObject object provides information the contained COM object. For each COM object
method, the ActiveXObject object creates an associated JavaScript Function object, and populates
attributes of that object with information about the method. These attributes

l allow ActiveXObject to identify the corresponding COM object method to call, and,

l provide information and advanced control of the method.

The Function object is a built-in JavaScript object that has these attributes:

Attribute

Description

_MEMBERID

Read-only integer that identiﬁes the method.

_INVOKEKIND

Read-only integer that identiﬁes the method type.

_DOCSTRING

Read-only string that represents the method name and parameter semantics.
[See“Examining a COM method’s signature and parameter semantics,” next.]

_PMODE

An integer that tells the method to run in synchronous mode (default), or in
parallel mode (a non-zero value). [See“RunningaCOMobjectmethodinparallel
mode” on page5.]

Examining a COM method’s signature and parameter semantics

The _DOCSTRING attribute describes the signature and parameter semantics of a method for a COM
object. Developers might use this attribute to examine the method’s signature to learn how to call
the method. For example, the ADODB.Connection COM object has an Open method that opens the
connection to the ADODB server. Using the ctxdriver utility, you can instantiate the object and
look at the value of the _DOCSTRING attribute:

1. Create connection, an ActiveXObject object that references an ADODB.Connection COM

object.

js> var connection = new ActiveXObject("ADODB.Connection");

2. Display the Open method by referencing it. (The ctxdriver utility returns the string

representation of the function when you reference it.)

js> connection.Open

function Open() {
[native code]

}

3. Examine the signature and parameter semantics of the Open method by referencing the

_DOCSTRING attribute. (The ctxdriver utility returns a string representation of the semantics
when you reference it.)

js> connection.Open._DOCSTRING
void Open( [in] BSTR ConnectionString, [in] BSTR UserID,
[in] BSTR Password, [in] long Options);

BroadVision, Inc.

One-To-One COM Extension

BroadVision One-To-One Enterprise COM Extension
Using the COM extension

5

Running a COM object method in parallel mode

By default, when you call the method of a COM object, that function runs in the Interaction
Manager’s serial mode and no other scripts may execute until that function call completes. For
example, the Work method of Sleep.Sleeper — a simple COM object — runs for a speciﬁed number
of seconds. While Work is running, the Interaction Manager is blocked and no other scripts can
progress.

<HTML><BODY>
<%
var sleeper = new ActiveXObject("Sleep.Sleeper");
sleeper.Work(10);
%>
<B>DONE</B>
</BODY></HTML>

// Block for 10 seconds

_PMODE

To run an object in parallel mode, set the _PMODE attribute to a non-zero value. For example, in the
following, the Work method runs in the Interaction Manager’s parallel mode and, does not block the
progress of other scripts.

<HTML><BODY>
<%
var sleeper = new ActiveXObject("Sleep.Sleeper");
sleeper.Work._PMODE = 1;
sleeper.Work(10);
%>
<B>DONE</B>
</BODY></HTML>

// Set parallel execution flag
// Work for 10 seconds

One-To-One COM Extension

BroadVision, Inc.

6

BroadVision One-To-One Enterprise COM Extension
ActiveXObject

ActiveXObject

The BroadVision One-To-One ActiveXObject component provides access to Component Object
Model (COM) objects running in the Microsoft Windows NT environment.

Method or attribute

Description

creator

creator

Creates an ActiveXObject object that is not bound to a COM object.

Creates an ActiveXObject object and binds it to an already instantiated
COM Automation object.

_bindToObject

Binds an already instantiated COM object to the ActiveXObject object.

Page

6

7

7

Moniker

An ActiveXObject component contains a reference to a COM object that has an IDispatch
interface. You should not have to know the details of COM or the IDispatch interface. Instead, you
only need to know either the registered name (ProgID) or moniker of the object desired, and that is
usually delivered as part of the object’s documentation.

A moniker uniquely identifies a COM object. Like a path to a file in a file system, a moniker
contains information that allows a COM object to be located and activated, without having any
other specific information on where the object is actually located in a distributed system. For
example, there might be an object representing a range of cells in a spreadsheet, which is itself
embedded in a text document stored in a file. In a distributed system, this object’s moniker
would identify the location of the object’s system, the file’s physical location on that system, the
storage of the embedded object within that file, and, finally, the location of the range of cells
within the embedded object.

ActiveXObject::creator

Creates an ActiveXObject object that is not bound to a COM object.

creator();

Return value

Returns a reference to the new, empty ActiveXObject object.

Parameters

None.

Remarks

Use this form of creator() to build a new, empty ActiveXObject object that will later be bound to a
COM object with the _bindToObject function. [See “_bindToObject” on page 7 for details.]

BroadVision, Inc.

One-To-One COM Extension

BroadVision One-To-One Enterprise COM Extension
ActiveXObject

7

ActiveXObject::creator

Creates an ActiveXObject object and binds it to a COM object.

creator( string servername.typename );

Return value

Returns a reference to the created ActiveXObject object.

Parameters

servername is the name of the application providing the object.

typename is the type or class of the object to create.

Remarks

Example

Use this form of creator() to instantiate, if necessary, and bind to the COM object. Do not use this
form to create an object that will later be bound with the _bindToObject function.

This example creates an ActiveXObject object based on the Scripting.Dictionary COM object, and
calls that object’s Add() method to add an entry to the dictionary:

var dict = new ActiveXObject("Scripting.Dictionary");
dict.Add("a", "Athens");

ActiveXObject::_bindToObject

Binds a COM object to the ActiveXObject object.

long _bindToObject(string Moniker);

Parameters

Moniker identiﬁes the COM object. [See “Moniker” on page 6 for more information.]

Return value

Zero (0) if successful; non-zero otherwise (see Error.reason for a description of the failure).

Remarks

Example

The binding process ﬁnds the object identiﬁed and, if necessary, puts it into the running state. The
object must have been created with creator(). This function should be called only once;
subsequent calls to this function always return true (0) for success.

This example binds an already instantiated Java object (java.util.Date) to date, which is an
ActiveXObject object. In this example the java object is being maintained by some other application,
possibly running in a Java Virtual Machine.

var date = new ActiveXObject();

// Use the Java moniker to "bind" to a Java java.util.Date object.
date._bindToObject("java:java.util.Date");

One-To-One COM Extension

BroadVision, Inc.

8

BroadVision One-To-One Enterprise COM Extension
Enumerator

Enumerator

The Enumerator component provides access a collection of items in a BroadVision ActiveXObject
object. (A collection is a group of related items that must be accessed sequentially; unlike a list
where the items can be accessed randomly.)

Method or attribute

Description

creator

atEnd

item

moveFirst

moveNext

Creates an Enumerator object.

Indicates whether or not the enumerator is at the end of the collection.

Returns the current item in the collection.

Resets Enumerator to point to the ﬁrst item in the collection.

Increments Enumerator to point to the next item in the collection.

Page

9

9

9

10

10

Example

This example shows how to use an Enumerator object to present a list of drives available on the
current system. It does that by creating an Enumerator to the Drives collection of a
Scripting.FileSystemObject COM object.

function ShowDriveList() {

var fso = new ActiveXObject("Scripting.FileSystemObject");
var e = new Enumerator(fso.Drives);
for (;!e.atEnd();e.moveNext())
{

var s = "";
var x = e.item();
var n;
s = s + x.DriveLetter;
s += " - ";
if (x.DriveType == 3)

n = x.

else if (x.IsReady)

n = x.VolumeName;

else

n = "[Drive not ready]";

s += n;
Response.write(s);
}

}

BroadVision, Inc.

One-To-One COM Extension

BroadVision One-To-One Enterprise COM Extension
Enumerator

9

Enumerator::creator

Creates an Enumerator object.

creator( ActiveXObject collection );

Return value

Returns the created Enumerator component, or null if an error occurred.

An Enumerator component is constructed using a ActiveXObject that is a collection. If the
_newenum attribute is deﬁned in the COM object, creator() returns an Enumerator object;
otherwise, if the attribute is not found, creator() generates an error (test with Error.set).

Parameters

collection is the existing ActiveXObject object to be used as the collection.

Remarks

See “Example” on page 8.

Enumerator::atEnd

Indicates whether or not the enumerator is at the end of the collection.

boolean atEnd();

Return value

Returns true if the current item is:

l the last item in the collection,

l the collection is empty, or

l the current item is undeﬁned;

otherwise, returns false.

Parameters

None.

Remarks

See “Example” on page 8.

Enumerator::item

Returns the current item in the collection.

BVI_Value item();

Return value

Returns the current item. If the collection is empty or the current item is undeﬁned, it returns null

Parameters

None.

Remarks

See “Example” on page 8.

One-To-One COM Extension

BroadVision, Inc.

10

BroadVision One-To-One Enterprise COM Extension
Enumerator

Enumerator::moveFirst

Resets Enumerator to point to the ﬁrst item in the collection.

void moveFirst();

Return value

None.

Parameters

None.

Enumerator::moveNext

Increments Enumerator to point to the next item in the collection.

void moveNext();

Return value

None.

Parameters

None.

Remarks

See “Example” on page 8.

BroadVision, Inc.

One-To-One COM Extension

