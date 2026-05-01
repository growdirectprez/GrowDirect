---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/tier1-md/arts/item-maintenance/ARTS XML Item Maintenance Charter.pdf.md
tags: [canary, arts, retail-data-model, standards-reference, tier1-extract]
project: canary
status: unprocessed
---

# ARTS XML Item Maintenance Charter.pdf

## Source
File: `Brain/raw/.extract/tier1-md/arts/item-maintenance/ARTS XML Item Maintenance Charter.pdf.md`
Size: 9,383 bytes

## Raw content
IXRetail Item Maintenance Work Team Charter

IXRetail

Item Maintenance

Work Team Charter

April 16, 2004

Copyright © National Retail Federation 2004.  All Rights Reserved.  This document may be copied or used for purposes consistent with adoption
of the ARTS Standards.  However, any changes or inconsistent uses must be pre-approved in writing by the National Retail Federation (“NRF”).
Consequently, this document may be furnished to others, but derivative works (the term “derivative works” does not include functional additions
that do not modify or change the base standard as written) that comment on or otherwise explain it or assist in its implementation may not cite or
refer to the standard, in whole or in part, without such permission.  Moreover, this document may not be modified in any way, such as by
removing the copyright notice or references to the NRF, ARTS, or its committees, except as needed for the purpose of developing ARTS
standards using procedures approved by NRF, or as required to translate it into languages other than English.

IXRetail  Item Maintenance Work Team Charter

TABLE OF CONTENTS

1.  REFERENCES....................................................................................... 3

2.  ABSTRACT ............................................................................................ 3

3.  TEAM NAME......................................................................................... 3

4.  MISSION STATEMENT ...................................................................... 3

5.  MEMBERSHIP ROSTER .................................................................... 4

6.  BUSINESS JUSTIFICATION .............................................................. 4

7.  BUSINESS SCOPE ................................................................................ 4

8.  USE CASE SURVEY............................................................................. 7

9.  PLANNED DELIVERABLES/DATES ............................................... 7

10.  REVISION HISTORY .......................................................................... 8

11.  ISSUES .................................................................................................... 8

12.  GLOSSARY............................................................................................ 8

Copyright © 2004 National Retail Federation All rights reserved.

Item Maintenance Charter04162004.doc.doc

Page 2

IXRetail  Item Maintenance Work Team Charter

1.  REFERENCES

•  NRF-ARTS Web Site (www.nrf-arts.org)

•  NRF-ARTS Data Model

•  NRF-ARTS IXRetail Technical Report: Best Practices – Schema Extensibility

2.  ABSTRACT

This document serves as the charter for the IXRetail Item Maintenance work team. The objective
of the Item Maintenance work team is to define a set of standard XML messages to communicate
common item information between applications in the retail enterprise.

3.  Team Name

The name of this IXRetail work team is Item Maintenance (IM).

4.  Mission Statement

The IXRetail item maintenance work team is charged with developing XML schemas for
exchanging item related data between systems within the confines of the retail enterprise. The
schemas are intended to be applicable across multiple retail vertical segments including general
merchandise, grocery, convenience, food and drug. The Item Maintenance work team will also
produce maps to and from selected, published item standards targeted at application-to-
application messaging within the retail enterprise.

Copyright © 2004 National Retail Federation All rights reserved.

Item Maintenance Charter04162004.doc.doc

Page 3

IXRetail  Item Maintenance Work Team Charter

5.  Membership Roster

Chair:

Tim Hood, Triversity, Inc.

Work Committee Members:

Monty Moncreif, Blockbuster
Frank May, Microsoft
Leonid Rubakhin, NSB
Dave Van Horn, SofTechnics

Work Committee Contributors:

Jay Heavilon, Mars Interactive
John Hervey, PCATS
Doug Jones, Target
Stuart McGrigor, ARTS
John Fluke, IBM
Richard Halter, ARTS

6.  Business Justification

The ‘item’ is the baseline element of retail; a retail enterprise exists to generate revenue from
items.

There is a very small number of systems in a retail enterprise (usually one) that expect to ‘own’
item data and a very large number of systems that require item data to fulfill their function. Item
data in most retail enterprises changes on a regular basis. Because of the large number of systems
involved and the frequency of change, a standard for communicating item information between
systems in a retail enterprise will provide huge benefits in system integration efforts applicable to
virtually all retailers.

7.  Business Scope

The following are to be considered within the scope of the team developing the first version of
the item maintenance schema:

•
Item attributes required for systematic functions
•
Item attributes required for communications between systems within a retail enterprise.
•  XSL Maps to/from equivalent standards ( for example UCC-EAN, NACS), relevant to

IXRetail target audience

•  The ability to create, update and delete item information in consuming applications
•

Items that are sold, in the past, present or future

Copyright © 2004 National Retail Federation All rights reserved.

Item Maintenance Charter04162004.doc.doc

Page 4

IXRetail  Item Maintenance Work Team Charter

•  A Publish-Subscribe paradigm (including file publication)
•  Heavy use of extension mechanisms
•  Absolute prices that are included as attributes of an item, including but not limited to:

(cid:190)  Manufacturer’s suggested retail price
(cid:190)  Cost
(cid:190)  Regular price (compare to)
(cid:190)  Selling price (permanent mark down)
(cid:190)  Price levels

The following may be considered within the scope of the Item Maintenance work team, but are
deferred for possible consideration in future versions of this specification or delegation to other
IXRetail work teams.

•

Item attributes require for communications of a B-to-B or Supply chain nature (to
systems outside of the retail enterprise)

•  Relationships between items (for example, shipping case vs saleable item within the case)
•
Item attributes required for customer facing activity (for example ad copy, images, selling
message, brand copy)
Item attributes of store fixtures and store supplies

•
•  A request-response paradigm
•
•  Definition or communication of the merchandise hierarchy (taxonomy)

Item attributes related to the design and development of product

Algorithms or rules which affect the price of an individual or collection of items are out of scope
of the Item Maintenance work team.

Algorithms or rules determining taxation of an individual or collection of items are out of scope
of the Item Maintenance work team.

Copyright © 2004 National Retail Federation All rights reserved.

Item Maintenance Charter04162004.doc.doc

Page 5

IXRetail  Item Maintenance Work Team Charter

Copyright © 2004 National Retail Federation All rights reserved.

Item Maintenance Charter04162004.doc.doc

Page 6

IXRetail  Item Maintenance Work Team Charter

8.  Use Case Survey

•  Multiple item add notification from item management system to consuming system
•  Multiple item update notification from item management system to consuming system
•  Multiple Item delete notification from item management system to consuming system
•  Compound message (multiple add, update, delete) notification from item management to

consuming system

9.  PLANNED DELIVERABLES/DATES

Prior to the May 2004 IXRetail Meeting

•  Submit Charter to Technical Committee for approval
•  Collect list of similar item maintenance standards
•  Collect attributes (identifier, type, text description/explanation)

At May 2004 IXRetail Meeting

•  Map contributed attributes to IXRetail XML dictionary
•  Select complementary standards Maps to be included in Version 1

Prior to August 2004 IXRetail Meeting

•  Collect attributes (identifier, type, text description/explanation)
•  Publish 1st draft of item schema

At August 2004 IXRetail Meeting

•  Finalize version 1 of item schema
•  Work on documentation

Prior to October 2004 IXRetail Meeting

•  Map IXRetail Item Maintenance schemas to selected industry standard item maintenance

schemas

•  Submit version 1 of item maintenance schema to IXRetail Technical Committee for

approval for public release

Copyright © 2004 National Retail Federation All rights reserved.

Item Maintenance Charter04162004.doc.doc

Page 7

IXRetail  Item Maintenance Work Team Charter

10.  REVISION HISTORY

Date

Name

Comments

March 10, 2004

Tim Hood, Triversity, Inc.

Initial draft

March 26, 2004

Tim Hood, Triversity, Inc.

Formated to IXRetail standards

April 16, 2004

Tim Hood, Triversity, Inc.

Updated with comments from work team

11.  ISSUES

1)  Need to identify the set of similar standards in order to define set of standards maps to be

produced by the work team

2)  Need to collect the widest ‘bundle’ of attributes, specifically covering as many verticals

between as many types of applications as possible

12.  GLOSSARY

Term

Definition

Copyright © 2004 National Retail Federation All rights reserved.

Item Maintenance Charter04162004.doc.doc

Page 8


## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
