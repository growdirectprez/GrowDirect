---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/Other Retek Decks/Retek Security.pdf.md
tags: [retail, retek, rms, rib, rdm, 2003-2005]
project: retail
status: unprocessed
---

# Retek Security.pdf

## Source
File: `Brain/raw/.extract/Other Retek Decks/Retek Security.pdf.md`
Size: 5,273 bytes

## Raw content
Retek Security

Retek security should be business driven. It is for this reason that Retek allows for complete customization
within all Retek applications for various security capabilities. The process for setting up Retek application
security involves identifying the tasks each user or group of users needs to perform, as well as the database
privileges these users need to perform the tasks. These privileges are then associated with user roles, which
can be assigned to users.  To ensure a secure database, it is important that users be granted no more access
than is necessary to complete their tasks.  We recommend security within Retek be set up at the database
level and the application level.

Retek provides the use of a additional level of Security and Maintenance, this is the creation of a User
Group Hierarchy. This gives clients the ability to aggregate Enterprise users into groups reflecting
supervisory roles (GMM, Store Manager, etc) and functional roles (buyer, planner, etc).  Parameter Driven
Groups can be used to support user aggregation by fundamental attributes (e.g., store number, department,
etc).  This functionality provides a framework for:
Language preference assignment
Advanced security  (application and data level)
Dynamic workflow and event routing
Enhancing  Oracle’s User and Role functionality

Maintenance for User Groups is provided for:

Supervision Hierarchy
Functional Hierarchy
Parameter Driven Groups

To ensure a secure database, it is important that users be granted no more access than is necessary to
complete their tasks.  We recommend security within Retek be set up at the database level and the
application level.

Database-level security involves setting up user roles with specific privileges to tables (such as the ability
to insert, update, select, and delete from specific tables).  The next step is to grant each user the necessary
user roles.

The application-level security provides access to various dialogs, menu options, and actions (such as new,
view, edit capabilities) according to the user roles.  For example, a ‘Supervisor’ user role may have full
order approval privileges; however, a ‘Clerk’ user role may only have the ability to create new orders and
modify existing orders.

1.0 Database-Level Security

1.1 Defining User Roles

To establish which user roles need to be created, first identify all of the users and the tasks they perform
(such as order maintenance, order approval, item setup and maintenance, etc.).  Next, split the users into
‘roles’ based on what tasks they perform (such as account clerk, account supervisor, inventory clerk,
inventory supervisor, developer, etc.).

Once the user roles are determined, privileges to insert, update, select, and delete from the database are
granted on a per table basis.  For each user role, it is necessary to assign privileges for each table in the
database.  For example, the user role of ‘Account Clerk’ may have the privileges to insert, update, and
select from the order header table, whereas the role of ‘Account Supervisor’ may have the privileges to
insert, update, delete, and select from the order header table.

Retek Confidential

1

5/28/2003

When planning security, define user roles so that all object and system privileges necessary to perform a
certain task are granted to a single user role.  After privileges are granted to a user role, the role can then be
granted to one or more users.  Utilizing user roles simplifies application maintenance, because adding a
new user requires granting one role, instead of granting all the individual privileges to each user.  Note that
multiple roles can be assigned to a single user.

Retek is delivered with two sample roles: ‘Buyer’ and ‘Developer.’  Please note that this is for development
purposes only.  In a production environment, roles should be created and granted privileges appropriate to
the client’s needs.

2.0  Application-Level Security

2.1  Limit User Access to Retek (Optional)

An optional step can be added to restrict users from accessing the Retek database through applications
other than the Retek application.  For example, a user may have the ability to go into the Retek application
to set up new items; however, that user should not be able to go into SQL*PLUS and manually insert
records into the item tables.

2.2  Hierarchy Forms

The merchandise and organization hierarchy forms contain the Retek Security program unit, which sets the
application-level security.  This program unit enables/disables buttons based on the values passed into the
program unit and the roles of the user.

The Retek Security program unit is called every time any of the action buttons are enabled or disabled. The
program unit will then check whether the user is authorized to perform the requested function and
enable/disable the buttons accordingly.

2.3  Search Forms

The search forms use the Retek Security program unit to determine the list elements in the drop-down list
boxes.

2.4  Menu Options

The menu options within the Retek applications can be customized based upon roles and User Groups. This
security can have the ability to add or remove menu items from the list of available items.

Retek Confidential

2

5/28/2003


## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
