---
date: 2026-04-22
type: raw
source: /Users/gclyle/secure/Dev Ops.pptx
tags: [secure, secure, loss-prevention, retail]
project: secure
status: unprocessed
---

# Dev Ops.pptx

## Source
File: `/Users/gclyle/secure/Dev Ops.pptx`
Size: 6,224 bytes

## Raw content
<!-- Slide number: 1 -->
# Secure 5 Agenda
Product 2018 Plans
Current 5.0 Program Status
Data Ingest Update
Delivery Responsibilities (open discussion)
Delivery Questions

<!-- Slide number: 2 -->
# Secure 5 Program Status
UAT and Configuration of the demo continues for the Secure Store 5.0 solution.
The Demo Solution is being treated as the first implementation and the product team is engaged to provide support throughout the process.
We expect the first Secure 5 project to be signed in the first quarter and the project should be spinning up soon.
The business goals for 2018 are targeted at 5 -6 new Secure 5 POS clients and 5 -6 Upgrades.
We are staffing Delivery and Dev Ops to be able to support 3 concurrent project streams with Product being involved in Dev Ops throughout.
The Dev Ops goal is to hand off full responsibility for deployments to the Delivery team by the end of the year (as judged by Delivery).
We are working toward a defined scheduled and moving to a roadmap driven product delivery cycle in 2018

<!-- Slide number: 3 -->
| Post Transaction Analytics Roadmap | 2018 Q1 – Available to Promise | 2018 Q2 | 2018 Q3 | 2018 Q4 |
| --- | --- | --- | --- | --- |
| Secure Store 5.x DevOps | Support the delivery team for Secure Store 5.0 (assuming 3 concurrent projects) | Support the delivery team for Secure Store 5.0 (assuming 3 concurrent projects) | Support the delivery team for Secure Store 5.0 (assuming 3 concurrent projects) | Support the delivery team for Secure Store 5.0 (assuming 3 concurrent projects) |
| Secure 3.x & 4.x | Support and hotfixes for Secure 3.x and 4.x | Support and hotfixes for Secure 3.x and 4.x | Support and hotfixes for Secure 3.x and 4.x | Support and hotfixes for Secure 3.x and 4.x |
| Technical Q&A | Support for testing and validating all development activities | Support for testing and validating all development activities | Support for testing and validating all development activities | Support for testing and validating all development activities |
| Secure Store | Secure Store 5.1 App |  |  | Secure Store 5.2 App |
| Secure Inventory |  | Secure Inventory 5.1 App |  |  |
| Secure Ecommerce | Secure Ecommerce Scope |  | Secure Ecommerce 5.1 App |  |
| Development Support for Real Time Decisions App | Incent 5.0 support | Verify 5.0 support | Verify 5.0 support | Verify 5.0 support |
# Product Roadmaps : Verify and Incent

<!-- Slide number: 4 -->
# Secure 5 Data Load Process

![](Picture9.jpg)
The ARDM data load and transform process provides data to the Secure and other Appriss retail products through a scheduled delivery of data differentials and updates
The Secure framework is dynamic and can support one or more POS data schemas independent of the data tier
Current testing is focused on a single tenant CRDM 1.8 schema residing on a SQL 2017 architecture
Work is still progressing on definition of the ARDM 1.0 schema in parallel
Secure Store POS 5.0 will ship with a CRDM 1.8 database, searchable, and metric generation process POS 5.1 will have CRDM 2.0
CRDM 2.0 will also include 2017 improvements such as Column Store Indexes and a review of new portioning capabilities
Data Science Team owns the Ingest Process and the Logical Schema definition of ARDM and CRDM, Product Team owns the implementation of CRDM, Maintenance, Searchables, and EBR metric generation process within the Secure Store application

<!-- Slide number: 5 -->
# Delivery Discussion / Questions
Q: With the introduction of the data team, how are projects run and managed gogin forward?
Delivery owns the project from end to end, providing project management, technical leadership, and application configuration as the team always has had
Although mapping is being handled by the data team, validation of the data, configuration and checking of metrics, definition of customer specific searches, and representation of the data in the application is a Delivery responsibility
Q: Customization (How far can we go):
The goal is to provide an off the shelf application to the customer that is repeatable and easy to deploy.  We will spend less time configuring customizations, there are defined roles in the app and out of the box dashboards for those roles as well as report and dashboard designers to put some of the customization aspects in the hands of the customer.
Customizing logon experience
Customizing emails/notifications coming out from the application
Any other customization possibilities, for example in transaction viewer
How to build complex reporting ( for ECM, Transaction based and for data load )Q: Upgrades  - Are there any tools considered to help Delivery in upgrading the client from Secure 3.x to Secure 5? How do we handle transferring questions / portals / monitors / pending items / cases? Are there corresponding functionalities in Secure 5?

<!-- Slide number: 6 -->
# Delivery Discussion / Questions
Q: Permissions – How to build data and functional restrictions in the system ( general discussion)
Is it possible to configure the application differently depending on the role AND location level restriction
Does the location level restriction work for every aspect of the system ( can we use them easily on custom reporting)

Q: Enterprise Case Management
Does ECM support location level restrictions?
BPM – How can we model process for retailers. i.e. Can we build workflows around approvals of a case easily?
3rd party integration – Do we build in 3rd party case integration in ECM?
Q: What sort of tools is the product team providing for delivery and support to enable us to identify if:
Are all the components of the system live – quick check of all the module hosts, RTIs and other components operational.
If there are issue – what is happening and were should we look if they are problems. Historically we have seen hard to understand logs coming out of the platform.
Is the system performing – easy to check metrics if the experience is within the designed parameters. This is for us during early deployments to be able to answer a question if system is slow or is the configuration a problem
Q: CCTV – Who owns it going forward?
Q: Cashier Coaching – Who will own it now? What are the plans for this?

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
