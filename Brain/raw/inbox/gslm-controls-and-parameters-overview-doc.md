---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/tier1-md/gslm/GSLM Controls and Parameters Overview.doc.md
tags: [canary, gslm, retail-data-model, walmart, comparison, tier1-extract]
project: canary
status: unprocessed
---

# GSLM Controls and Parameters Overview.doc

## Source
File: `Brain/raw/.extract/tier1-md/gslm/GSLM Controls and Parameters Overview.doc.md`
Size: 3,253 bytes

## Raw content
The Controls and Parameters entities contain logical constructs to help with the physical build and deployment of interfaces. The movement of data which will be contained in this logical model will flow across a variety of interfaces, when this data flows there will be interface file specific attributes which need to be added to the logical data. For example, an interface file may require that a sequence number must be incremented through each interface instance. This sequence number has no place in the logical functional model so it can be captured in the controls and parameters area. Controls and Parameters contains a number of entities to hold this and related interface attributes.
The controls and parameters model has been defined as a generic structure. Many of the attributes contained in this model will be of use to interface developers however not all will always be needed.
It is foreseeable that the control and parameters data model will be extended when physical interfaces are produced. In respect of this the governance model around the control and parameters entities is recommended to be less strict that that of the functional areas of the logical model.

The following section describes the GSLM entities and their attributes which have been modeled as part of the Controls and Parameters scope.

EntityName
Description
Interface
The entity that describes the high level information of the interface
Attribute
Type
Description
interface_id
 Number
The unique interface number
interface_description
 Text
A description of the purpose of the interface
interface_type
 Code
An interface type identifier (batch, realtime, pub/sub etc)
suspend_contact_type
 Code
What or who to contact in the event of a suspension (system, person, team)
suspend_contact_mechanism
 Code
A way of notifying of suspension (Email, LogFile, Pager)
suspend_contact_notification_address
 Text
A notification address to contact



EntityName
Description
LocationInterfaceSchedule
The schedule of the interface by sales outlet
Attribute
Type
Description
interface_id
 Interfaces
The unique interface number
location_id
Locations
The target location identifier
next_run_time
 DateTime
The scheduled time for the next interface run
retry_count
 Number
The number of times and interface should retry in the event of failure
retry_delay_between_retry
 Number
The delay in between retry's in the event of failure
interface_counter
 Number
A unique counter which may be used by an interface



EntityName
Description
Dependency
The dependencies on interfaces
Attribute
Type
Description
interface_id
 Interfaces
The interface that is dependent on something
dependancy_id
Interfaces
The interface that is the dependency
sales_outlet_id
SalesOutlet
The Sales Outlet that this dependency occurs for



EntityName
Description
LocationInterfaceSpecificValue
A generic entity to hold interface specific information
Attribute
Type
Description
interface_id
 Interfaces
The interface that has attributes
location_id
Locations
The location that this attribute refers to
attribute_name
 VarChar
The attribute name
attribute_value
 Text
The attribute value
attribute_desc
Text
Extended text description









Global Store Logical Model – Controls and Parameters




## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
