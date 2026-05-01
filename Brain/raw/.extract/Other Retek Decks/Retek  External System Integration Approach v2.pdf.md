Retek® Integration Bus™

The Recommended Approach for
External System Integration

Retek Integration Bus

The software described in this documentation is furnished under a license
agreement, is the confidential information of Retek Inc., and may be used
only in accordance with the terms of the agreement.

No part of this documentation may be reproduced or transmitted in any form
or by any means without the express written permission of Retek Inc., Retek
on the Mall, 950 Nicollet Mall, Minneapolis, MN 55403, and the copyright
notice may not be removed without the consent of Retek Inc.

Information in this documentation is subject to change without notice.

Retek provides product documentation in a read-only-format to ensure
content integrity.  Retek Customer Support cannot support documentation
that has been changed without Retek authorization.

Retek® Integration Bus™ is a trademark of Retek Inc.

Retek and the Retek logo are registered trademarks of Retek Inc.

This unpublished work is protected by confidentiality agreement, and by
trade secret, copyright, and other laws. In the event of publication, the
following notice shall apply:

©2003 Retek Inc. All rights reserved.

All other product names mentioned are trademarks or registered trademarks
of their respective owners and should be treated as such.

Printed in the United States of America.

Corporate Headquarters:

Retek Inc.

Retek on the Mall

950 Nicollet Mall

Minneapolis, MN 55403

888.61.RETEK (toll free US)
+1 612 587 5000

European Headquarters:

Retek

110 Wigmore Street

London

W1U 3RW

United Kingdom

Switchboard:

+44 (0)20 7563 4600

Sales Enquiries:

+44 (0)20 7563 46 46
Fax:  +44 (0)20 7563 46 10

Retek® Confidential

Customer Support

Customer Support hours:

Customer Support is available 7x24x365 via e-mail, phone, and Web access.

Depending on the Support option chosen by a particular client (Standard,
Plus, or Premium), the times that certain services are delivered may be
restricted.  Severity 1 (Critical) issues are addressed on a 7x24 basis and
receive continuous attention until resolved, for all clients on active
maintenance.

Contact Method  Contact Information

Internet (ROCS)   www.retek.com/support

E-mail

Phone

Mail

Retek’s secure client Web site to update and view issues

support@retek.com

US & Canada: 1-800-61-RETEK (1-800-617-3835)
World: +1 612-587-5800
EMEA: 011 44 1223 703 444
Asia Pacific: 61 425 792 927

Retek Customer Support
Retek on the Mall
950 Nicollet Mall
Minneapolis, MN 55403

When contacting Customer Support, please provide:

•  Product version and program/module name.

•  Functional and technical description of the problem (include business

impact).

•  Detailed step by step instructions to recreate.

•  Exact error message received.

•  Screen shots of each step you take.

Contents   i

Contents

Retek® Integration Solution™ and Technology Partnerships
.................................................................................................. 1

The Recommended Approach for Integrating EAI Tools to
the RIB...................................................................................... 1

Other External Integration Alternatives ................................ 4

I.  SeeBeyond® e*Way™ Intelligent Adapters & e*Gate™  Add-ons .............. 4

II.  Integration Service Offerings Provided By Retek......................................... 5

III. EAI Replacement .......................................................................................... 6

The Recommended Approach for External System Integration   1

Retek® Integration Solution™ and Technology
Partnerships

The Retek 10™ releases of the Retek Integration Solution™ (RIS) include application
interfaces using the Retek Integration Bus™ (RIB) for the Retek Merchandising
System™ (RMS), Retek Customer Order Management™ (RCOM), Retek Distribution
Management™ (RDM) and the Retek Integrated Store Operations (RISO) Retek Store
Inventory Management (RSIM) solutions.  The Retek® Integration Bus™ is based on the
products of Retek’s preferred EAI partner SeeBeyond®.  Its architecture supports
integration to external systems through integration with the RIB.

In conjunction with Retek Integration Solutions, the Retek Technical Partner Program
(RTPP) assists Retek technology partners by standardizing and expediting the way in
which they integrate or interoperate with Retek applications. The program is intended to
provide technical partners with clearly defined options for developing solutions related to
Retek solutions.  This program represents an effective way to offer Retek software to
technology partners with associated maintenance and support options. The RTPP, will
enable technical partners to offer their customers a reliable product that is validated with
Retek software for optimal use at a client site.

The Recommended Approach for Integrating EAI
Tools to the RIB

A client may choose to contract directly from alternate Enterprise Application Integration
(EAI) vendor (e.g. IBM, WebMethods, BEA and Vitria), building interfaces directly to
the SeeBeyond based Retek Integration Bus (RIB) solution.

The key to message based integration between the RIB and another EAI vendor is to
construct a bridge  between SeeBeyond e*Gate™ Java Message Service (JMS) and that
of another vendor.  The purpose of the bridge application is to simply copy messages
from one JMS implementation to another.

2   Retek Integration Bus

The Java Message Service is a J2EE core facility used for messaging.  As per the
philosophy of J2EE, the JMS is defined by a set of standards and not by a specific
implementation.  As such, multiple implementations of JMS providers exist from a
variety of vendors and Open Source initiatives.

Most JMS providers come bundled with a specific J2EE compliant application server.
However, if the JMS implementation is compliant to the appropriate standards, then this
bundling becomes irrelevant and Java clients running outside of the application server
can use the JMS services.  If the J2EE application server is also compliant with the
appropriate standards, then it may use any standard compliant JMS provider.

Retek preferred EAI provider, SeeBeyond®, has implemented a JMS that is nearly
standards compliant.  Retek has successfully implemented with the JBoss and IBM®
WebSphere™ application servers, and SeeBeyond has experience implementing its JMS
with the BEA Systems® WebLogic™  application server.  Conversely, the SeeBeyond
e*Gate integrator has configuration entries that allow using another vendor’s JMS
provider.

But simply having one system to place messages onto another’s JMS implementation (i.e.
the bridge) is not the most difficult aspect of external EAI  integration.  What is needed
are compliant JMS factory classes and a way to instantiate these classes.  The most
difficult part is found in the format, content, and semantics of the messages that are
published and subscribed to.  Retek has invested a considerable amount of time and effort
in defining messages specific to its applications.  One can assume that the same is true for
non-Retek messaging systems.  Because software designers and architects rarely
independently arrive at the same design and implementation, one can expect differences
in all three facets of a message:  its format, content, and  semantics.  Hence it can be
expected that a bridge application of some sort will be needed even if both JMS
implementations, the SeeBeyond e*Gate framework and the J2EE application server
framework have absolutely no problems interoperating with each other.

The Recommended Approach for External System Integration   3

The problems found in external EAI integration are similar in nature to those found in
Legacy integration.  Both require a format manipulation from one message representation
to another.  A translation may be needed from the Retek hierarchical XML format to a
fixed field length (aka flat file) format, to an alternative XML representation, or even
may be encapsulated into a Java object that is published as a stream of binary data.
Another problem lies in the data contents found in a message.  For its transactional
messages, Retek publishers assume that  certain data, commonly known as “Foundation
Data”, has been communicated and is available to all of its subscribers.  If this data is not
available, then the Retek message must be augmented in some fashion specific to the
needs of the subscriber.  Furthermore, even if the data exists in the non-Retek system, it
may need to be referenced using a different code value.

For integration, all that is needed are compliant JMS factory classes and a means to find
and / or initiate the classes once careful work has been performed to equate message
formats, contents and semantics for publication and subscription.  Retek has defined,
constructed, validated and delivered messages specifically designed for the retail industry
and the Retek applications.

In this instance, Retek supports the RIB if no changes are made to the RIB integrated
products as part of the integration construction.  For issues with the vendors adapters or
the external integrated systems, Retek will act as the single point of contact, forwarding
issue inquiries to support staff of application vendor.  A client may also choose to
contract additional, extended licensing from the vendor.  Integration components of the
alternate EAI and / or ETL applications to the RIB and / or RETL components are not
supported by Retek unless contracted through Retek Services with an appropriate support
agreement.

4   Retek Integration Bus

Other External Integration Alternatives

I.  SeeBeyond® e*Way™ Intelligent Adapters & e*Gate™

Add-ons

The RIB is delivered to clients purchasing the Retek 10 releases of RMS, RDM, RCOM
and / or ISO products.  As part of the RIB delivery, clients have the option to choose two
additional connection methods.  Clients may choose from e*Way™ Intelligent Adapters
and / or e*Gate™ Add-ons for systems such as Oracle® Financials™, IBM WebSphere®
MQ family and many others.  For issues with the SeeBeyond adapters or the external
integrated systems, Retek acts as the single point of support contact, forwarding issue
inquiries to the SeeBeyond support staff or other application vendors.  Retek supports the
RIB adapters but not the SeeBeyond adapter.  A client may also choose to contract
additional, extended licensing from SeeBeyond and / or the other application vendor.

Clients should contact Retek to request the external system connections.  Clients are
responsible for configuring the SeeBeyond adapters and are responsible for building and
testing the integration between the SeeBeyond adapters and the external application.  As
a result, implementation of the SeeBeyond adapters may necessitate work by Retek
Services.

The Recommended Approach for External System Integration   5

II.  Integration Service Offerings Provided By Retek

A Client may contract from Retek several optional integration service offerings.  These
offerings would be constructed and supported by Retek.  They include construction of:

1  acy / vendor system harnesses that allows a client to convert Retek Integration Bus
(RIB) XML messages from and to flat file, ‘legacy’, formats.  Integration between
these platforms is attractive, because the client may stage how and when they
upgrade their systems.  The client may take advantage of the RIB messaging
capabilities while integrating their current logistics system with standard file formats.
This effort does not seek to invalidate any existing implementation, but to provide
tools for the client to extend its existing mechanisms and investment;

2  Legacy / vendor system cross-reference / translation layers that provide an engine

that, in the most basic terms, accepts an object Id from a legacy system, and translate
that to the corresponding object Id for input to Retek products.  Our solution will
provide the implementations of generic classes and methods while also providing
hooks that will allow clients to implement, configure, more complex, customized
scenarios;

3  Financial system integration that provides clients with custom integration between

Retek, client legacy and application provided by third party vendors such as Oracle®
Financials™, PeopleSoft® Financial Management Solutions™, SAP® mySAP
Financials™, Lawson® Financials Suite™ and / or other financial packages.  The
standard Retek option for integration to third-party financial applications is through
use of the SeeBeyond adapters (noted above with the first integration option).  If,
however, a client requires integration beyond the two connection point  solution, this
service offering will provide the added financial system integration;

4  Custom message payloads that provide clients with RIB message payloads.

Currently, the standard RIB message payloads contain Retek defined data tags.
These tags may be insufficient for integrating client systems to support the full array
of their business processes.  Custom message payloads would provide solution for
client business process integration not currently supported by generally available,
‘base’, Retek product solutions.

6   Retek Integration Bus

III.  EAI Replacement

A client may choose from a variety of options for complete replacement of EAI and / or
ETL tools.  This is entirely at the discretion of the client and should be preceded by an in-
depth study of return on investment.

Retek does not recommend this approach due to several cost of ownership factors
that must be evaluated by the client.  The costs that may be incurred by not using the
generally available SeeBeyond-based solution include:

•  Business requirements analysis, design, construction, test and implementation costs

associated with initial replacement of the SeeBeyond components;

•  Additional maintenance expenses associated with the need for Retek support

agreements as well as agreements with the other EAI providers.  With the single
Retek solution, Retek support has a total view over all components of the integrated
solution and the inherent ability to manage and resolve integration issues regardless
the root cause.  With a fragmented integration solution, resolutions may not be
identified or defined created as easily or as quickly;

•  Design, construction, test and implementation expenses incurred as a result of not

being on the generally available Retek upgrade path.

If, however, the client chooses this alternative, the client would:

1  Entirely replace their existing EAI implementation with SeeBeyond products and / or
use the RETL instead of other ETL tools.  Support, maintenance and / or services
provided for the additional interfaces (that are not generally available interfaces
delivered by Retek) would require an additional agreement between the client, Retek
and possibly SeeBeyond;

2  Contract directly from an alternate (non-SeeBeyond) EAI and / or ETL vendor to
completely replace the RIB SeeBeyond and / or RETL components with solutions
provided by the alternate provider.  The Retek product portion of the integration
would be supported but all components of the alternate vendor product would not be
supported by Retek unless support, maintenance and / or Retek Service agreements
were reached between the client, Retek and / or the tool vendor;

3  Construct an alternate integration architecture, such as replacing the message based

interfaces with other integration mechanisms such batch / flat-file solutions.
Replacement of the SeeBeyond, RIB and / or RETL components or construction of
alternate integration components is not supported by Retek unless an agreement is
reached between Retek and the client.

