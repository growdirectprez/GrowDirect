	3.Integration 
	3.1.Internal integration
Internal integration of the various Retek modules proposed is achieved through the Retek Integration Solution™ (RIS). This solution makes use of both application interfaces using the Retek Integration Bus™ (RIB) and ETL (RETL) based techniques in order to both eliminate single point of failure and support distribution of application components. The Retek® Integration Bus™ is based on the products of Retek’s preferred EAI partner SeeBeyond®. Its architecture also supports integration to external systems through integration with the RIB. Retek has developed a set of adapters and messages that allow an enterprise to integrate both Retek and non-Retek applications together in a cohesive, scalable, and supportable fashion.




The RIB software is distributed in a single messaging schema. This schema contains all of the RIB’s publishing and subscribing e*Ways (adapters) and Connection Points. It also contains a single JMS Intelligent Queue Manager.

One feature of the RIB is the Error Hospital subsystem used to store and retry messages that have processing problems by a subscribing application. This facility allows for non-dependent messages to continue to be processed by the application until the failure has been resolved and the message successfully consumed.

In SeeBeyond’s Enterprise Application Integration (EAI) environment, a “Registry” embodies a complete administrative domain. A Registry is a database defining the deployed EAI system and a program that controls access to this database. A Registry is organized into one or more Schemas. Each schema details a collection of e*Ways, BOBs, Intelligent Queue Managers, Intelligent Queues, Connection Points, and Collaboration Brokers along with their network addresses or locations. The Registry also contains basic security objects that control user identifications, roles, and privileges shared across all schemas. Because the Registry embodies all configurable parameters, no other component can be brought up without access to a registry, either directly or indirectly.

Deploying and configuring “Secondary Registries” can alleviate these problems. Secondary Registries replicate the Primary Registry. The replication of the configurations occurs transparently during normal operation of the system.

If the host containing the primary registry fails, SeeBeyond will automatically fail over surviving control brokers to the secondary registry.




Questions from Birgitta:

For which transactional messages do you assume that”certain data, commonly known as ”Foundation Data”” has been communicated and is available to all of its subscribers?
Please specify what Foundation Data that this refers to. 
We would like to specify this with Åhlens during the Technical meetings in late September and in the beginning of October.

External integration

1. Approach to external integration and supported integration layers:
2. Existing integration points and supported message formats:
As mentioned in 21.1 Retek makes use of an integration solution called RIS , which is composed of two elements, namely RIB and RETL.

The Retek Integration Bus (RIB) is Retek’s application integration message processing for its retail application suite. Using SeeBeyond Technology Corporation’s e*Gate Integrator EAI platform as a base, Retek has developed a set of adapters and messages that allow an enterprise to integrate both Retek and non-Retek applications together in a cohesive, scalable, and supportable fashion.

The key to message based integration between the RIB and another EAI vendor is to construct a bridge between SeeBeyond e*Gate™ Java Message Service (JMS) and that of another vendor. The purpose of the bridge application is to simply copy messages from one JMS implementation to another.



The Retek Extract Transform and Load (RETL) is a tool used in parallel processing systems where high volumes of data must be processed quickly. By incorporating RETL into an application, the amount of time required to process data from databases and flat files may be reduced. RETL fully utilizes all available processors and by increasing the number of processors on Unix servers it can scale to handle larger volumes of data. As the name suggests the utility allows the extraction of data from a database or flat file, the transformation of that data on-the-fly and the insertion of the transformed data into a database or into a flat file. Code is written in XML – much easier to code than Pro*C, C and Java. Existing XML tools can be used to help in the development process.

3. Openness of Application and Message Formats:
The Java Message Service is a J2EE core facility used for messaging. As per the philosophy of J2EE, the JMS is defined by a set of standards and not by a specific implementation. As such, multiple implementations of JMS providers exist from a variety of vendors and Open Source initiatives.

Most JMS providers come bundled with a specific J2EE compliant application server. However, if the JMS implementation is compliant to the appropriate standards, then this bundling becomes irrelevant and Java clients running outside of the application server can use the JMS services. If the J2EE application server is also compliant with the appropriate standards, then it may use any standard compliant JMS provider. Retek preferred EAI provider, SeeBeyond®, has implemented a JMS that is nearly standards compliant. Retek has successfully implemented with the JBoss and IBM® WebSphere™ application servers, and SeeBeyond has experience implementing its JMS with the BEA Systems® WebLogic™ application server. Conversely, the SeeBeyond e*Gate integrator has configuration entries that allow using another vendor’s JMS provider.

The problems found in external EAI integration are similar in nature to those found in Legacy integration. Both require a format manipulation from one message representation to another. A translation may be needed from the Retek hierarchical XML format to a fixed field length (aka flat file) format, to an alternative XML representation, or even may be encapsulated into a Java object that is published as a stream of binary data. Another problem lies in the data contents found in a message. For its transactional messages, Retek publishers assume that certain data, commonly known as “Foundation Data”, has been communicated and is available to all of its subscribers. If this data is not available, then the Retek message must be augmented in some fashion specific to the needs of the subscriber. Furthermore, even if the data exists in the non-Retek system, it may need to be referenced using a different code value.

For integration, all that is needed are compliant JMS factory classes and a means to find and / or initiate the classes once careful work has been performed to equate message formats, contents and semantics for publication and subscription. Retek has defined, constructed, validated and delivered messages specifically designed for the retail industry and the Retek applications.

4. Documentation and Integration points:
RIB 10.2 contains over 30 message families and these are all documented and explained in the system documentation provided with the purchased applications: A number of these are listed below. Essentially, RIB Message Families contain information specific to a related set of operations as well as business entities.  Message Families:
Merchandising
- Items, Locations, Hierarchies, Purchase Orders, Vendors, Allocations, Transfers, User Defined Attributes …
 Distribution Management
- ASN, Appointments, Return to Vendor, Space Locations, Receipts (Bill of Lading), Stock Order Status, Order Release, Inventory Adjustments, Inventory Balances, …
 Customer Order Management
- Order reserve, Sale, Return …
 Externally published
- Chart of Accounts, Freight Terms, Currency Rates, Vendors, Payment Terms, …


RETL contains the following Operators: 
Import Operators
Oraread
Perform the read operation of data out of the Oracle database.

Export Operators:
Orawrite
Perform the load operation of an RETL dataset into the Oracle database.



