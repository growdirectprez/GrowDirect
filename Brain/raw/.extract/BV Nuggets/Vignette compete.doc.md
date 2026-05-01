Competitive Brief
Vignette

This is a BroadVision internal document. Only Section 2 of this document may be shared with customers when they ask us for our view of Vignette.
1. How to compete with Vignette
When competing with Vignette it is critical to keep the bar high.  The problem facing organizations today is bigger than content publishing - it is effectively capturing AND distributing information; it is increasing employee productivity; it is managing online relationships; it is integrating the web into your business activities.  Content publishing is part of the story.  Vignette is a point solution for publishing content and does not solve the above problems.

True relationship and knowledge management applications requires four steps:
Capture - the ability to capture content.  Document Management Systems (Lotus, Documentum) are strong here.
Publish - making content available.  This is Vignette, as well Lotus, Documentum, and a host of others.
Distribute - get content to right people at right time.  This would include physical distribution (push, email, web) as well as logical distribution, or the ‘right content’ (matching, targeting, search)
Act - the ability to accept action as a result of knowledge distribution, such as a transaction, an observation, an information request, etc.
Only BroadVision offers a complete solution to this problem; Vignette solves only the “Publish” step. 

Stress BV’s true value proposition - relationship management - and BV’s true competitive advantages - dynamic control, personalization, transactions, and architecture.  

Be prepared to defend and show our publishing strengths in the demo. Show PC Inc for strengths in knowledge management and do publishing as part of that demo.
2. How BroadVision positions Vignette
BroadVision favorably compares against Vignette in four main areas:
Application functionality
Relationship Management
Architecture
Publishing functionality

(Note: This section can be cut and pasted for delivery to prospects and customers)
A. BroadVision is an application; Vignette is a publishing platform
BroadVision provides enormous value in out-of-box functionality for building sites whereas Vignette is a publishing platform from which you must custom build features for a site.  Examples of BroadVision out-of-box features include:
content alerts
email targeting
content bookmarking
One-To-One Knowledge channels
Distributed channel management
Channel subscription
Personal channels
Verity search 

In short, these One-To-One Knowledge features, supplemented with Commerce and Financial functionality, make BroadVision an application and Vignette a platform.

Implications: 
longer development times and increased costs for creating or integrating desired features

B. Relationship management is more than publishing
Vignette is great for publishing content on a web site that looks the same for everyone. For relationship management you need user profiling, personalization, learning relationships, business manager control, transactions and external system integration. Vignette is great at publishing an on-line newspaper but not a relationship management site. BroadVision provides a complete suite of relationship management applications (Knowledge, Commerce and Finance) and the tools needed to manage those applications.
Lets see how Vignette does in each of the areas of relationship management:
Profiling: there is no profile database. Profiling within Vignette is at best limited to cookies.
Personalization: there is no out-of-the-box support for personalization. Their partnership with Open Sesame and NetPerceptions provides is collaborative filtering which is black box personalization. Whereas, BroadVision provides nine types of personalization capabilities out-of-the-box (rule-based matching, agent matching, moment-to-moment personalization, feedback, learning, voting, alerts, menu select, attribute search and text search) and an open architecture that can integrate with other personalization tools. We have already done this with NetPerceptions.
Learning relationships: learning is a key part of managing relationships with customers. Vignette has no support for tracking observations.
Business manager control: just like a business in the real world on the Net the business manager needs to be in control. Vignette has no support for business rules. To change the behavior of a page you have to change the template. With BroadVision this can be done dynamically through the DCC. With BroadVision’s new Knowledge Management application, business managers can now change the site structure, rules and content dynamically.
Transactions: relationships are more than information exchange. They are about conducting real transactions, such as buying, selling and customer service. Vignette has nothing like BroadVision’s robust commerce server and a financial server for soft/hard goods and financial services respectively.
External system integration: a relationship management system needs to tie to external systems, such as external content sources ala Lotus Notes and Documentum, external applications ala HRMS, sales force automation, customer support and enterprise resource management applications. Vignette has no out-of-the-box support or experience in this area. Whereas BroadVision has been architected from the ground up for integrating with external systems and we have a wealth of experience integrating with DB2, CICS based applications, middleware packages like Tuxedo, Tibco and MQ-Series, and transaction backbones like Integrion banking system and airline reservation systems.
C. Architecture and scalability
N-Tier vs Two Tier: an enterprise scale application needs an N-Tier architecture with the following tiers: presentation logic, business logic, application logic and data. This allows users with different skills and tasks to independently work on the application. For example, template designers should be able to work independent from the programmers and the business managers. 

Vignette has a two tier architecture namely templates and database. Presentation, application and business logic are all on the template in the form of HTML and TCL. Writing a dynamic application with Vignette is no different from stage one web-sites that used Perl.

Implications: 
Programmers, template designers and business managers need to coordinate changes. 
All need to know how to write TCL (how many business managers do?) or go through the change-request queue of IT programmers. 
Changing the application cannot be done dynamically.

Performance and scalability: an enterprise scale application needs to be designed with end-to-end performance in mind. Which means that if you have a page that requires access to an external system then you need to optimize the performance of the whole system not just the page serving performance. 

Caching: is a key part of scalability. Vignette does caching by pre-generating the entire page. Whereas, BroadVision caches the content and the data so while each page can be personalized we don’t have to access the database each time.

Implications: 
This scheme works only if the content is all static. If even one element of the page is dynamic, for example, based on time or a database lookup, then the page needs to be re-generated. Since Vignette does not cache content or data or connections this will slow down their system by a factor of 10 or more. 
For personalized pages there can be a lot of combinations and it may not be practical to pre-generate all the combinations. For example, if the TCL script is based on six parameters each with ten values then you are need to pre-generate a million pages (10*10*10*10*10*10).

Closed  system: Vignette’s design center is content and templates stored in their database.  

Implications: 
If you want to change a template using a third party HTML editor, you have to first open up the template in Vignette’s tool, copy and paste to the HTML editor, make your changes and copy them back to Vignette’s tool.

D. Publishing
Weak remote publishing: unlike BroadVision’s Content Management Center Vignette does not have an out-of-the-box web-based publishing tool. Instead, customers have to create their own templates for managing content. None of the publishing functionality is available through the web like workflow, in-box and locking. For example, because no locking is available from the publishing templates you could override someone’s changes without knowing it. To preview a template you need to be running on the same platform that created the template. So if you created the template on a Sun machine then you must run your browser on that machine to preview the content.
Implications: 
You have to pay Vignette consultants to build publishing templates
It would be very hard to manage content publishing process where third-parties or employees are entering content remotely
Weak document publishing. Vignette’s design center is HTML based story publishing but is weak for non HTML content. For example, there is no support for uploading documents in their publishing tool. You have to upload the document yourself on the web-server, then go to Vignette’s tool and associate the uploaded file path with a content item. If you want to make a change to a document associated with a Vignette content record then you have to download the document yourself, make the edits and upload it yourself outside of Vignette.
Implications: 
It would be very hard to use Vignette for knowledge management applications where documents (like Word, Powerpoint, etc) need to be published and distributed.
No content type:  Vignette has no understanding of how a "product" piece of content differs from "advertisement" content. Whereas, BroadVision provides out-of-the-box support for six types of content - ads, editorials, products, incentives, templates and discussion groups.
Implications: application needs to custom define content type semantics
A file, content, or template cannot be associated with more than one project. It must be physically copied. 
Implications: The potential for redundancy and duplication of content is very high.  Requiring redundancy means duplicate maintenance when changes are made.
No built-in metaphor for content organization: unlike BroadVision Vignette has no ability to categorize or in any way organize content. Content categorization is important in many scenarios. For example, a store may organize products along departments and sub-departments, a knowledge-base may organize content along customer and channel segments. Whereas, BroadVision provides two metaphors of organizing content: categories and channels, which make it easy for the end-user to view the content.
Vignette supports simplistic workflow scenarios only where the workflow is a linear set of states. Unlike BroadVision no support is provided for branching or complex workflows that will be required for iterative and conditional edit/approve steps. For example it would be hard to model a workflow such as follows: if the content has pricing information then it needs legal approval otherwise it can go straight to copywrite.
3. How Vignette’s positions BroadVision
BroadVision is too expensive
BroadVision is too complex/expensive to develop sites
BroadVision is not modular; is all or nothing solution.  
One-To-One personalization is inherently slow
BroadVision does not support project-oriented content management
BroadVision does not have a unified tool for content, template and project management

Response to Competitor’s criticisms of BroadVision
BroadVision is too expensive.  Vignette is not a cheap solution - ASP for software is north of $80K with additional $100K for consulting. Vignette only delivers a content publishing platform.  One-To-One Knowledge delivers a complete knowledge management application, which would require extensive development and integration for Vignette.
BroadVision is too complex/expensive to develop sites.  For  knowledge management and content publishing, BV KWA and CMC provides a complete solution, requiring no additional development. Customers can bring up knowledge based sites in as little as two weeks. Vignette is quoting large integration and implementation efforts for BV systems.  This is misleading as the implementation efforts are for integrating into multiple backend legacy systems - something that would be more difficult and costly using Vignette. 
BroadVision is not modular; is all or nothing solution.  Wrong.  In addition to providing a functionally complete knowledge management solution with KWA, BroadVision also has a completely open architecture which allows the integration of best-of-breed technologies. For example, we have integrated with Lotus Notes and Documentum for content, and NetPerceptions for collaborative filtering.
One-To-One personalization is inherently slow, they claim, on the basis that each page has to be regenerated for every customer. Vignette claims that because they cache generated pages they only have to re-generate the pages that have changed. But this approach only works for dynamic sites not personalized sites. BroadVision’s finer grained caching of content and profile leads to higher performance for both personalized and dynamic sites.
BroadVision does not support project-oriented content management, i.e. the ability to define projects to coordinate changes to a site. These changes at a project level before they are promoted to the live site. BroadVision scheduling calendar provides a high-level view into what content is being scheduled for when. We are adding support for simple reports that enable editors to get a glimpse into who is working on what.
4. Vignette Company Background
Product
Story Server (version 3.2)

Pricing
Development Licenses:	starting at $20K
Deployment License	starting at $40K
ASP:			$183K ($83K software, $100K services)

Positioning
Vignette positions themselves as the premiere Web content application platform for building, managing, and delivering service-based applications, such as online, publishing, knowledge management and sophisticated e-commerce systems for corporate Internets, intranets and extranets. In reality what they provide is a web-publishing tool.
Strengths
Strong publishing background and story.  They have productized a custom effort generated at CNET.  High profile publishing customers, such as Tribune Interactive, PC World, MecklerMedia, Playboy, Time Warner Pathfinder, ZDNet.
Robust content publishing environment.  Support for workflow, content staging, access control, content triggering, integration with Macromedia Dreamweaver for HTML creation; support for XML
Multi-Platform support.  Vignette now runs on Solaris and NT operating systems; Oracle, Sybase, Infomix, SQL Server databases; NS Enterprise, MS IIS, Apache web servers.
Template debugging environment.  Vignette now provides full debugging support for template creation.
Quick implementation with some sites going live within two weeks
One unified tool that combines template management, content management and project management
General Background
Founded in December of 1995. Released the first product (StoryServer) January 1997 with revenues the first year of $5.6mm and revenues  anticipated at $15mm-$20mm next year.
Currently recruiting for CEO and VP Marketing. Existing CEO and VP Marketing have taken other positions within Vignette.
Raised the largest round of venture capital backing in Austin, to date ($13.5mm).  Funding is from Adobe Ventures LP,  Attractor Investment Management, Austin Ventures, CNET: The Computer Network, and Sigma Partners. The company is about 100 employees today growing to 150 by year end.
The sales force (2 Sales Managers, 7 Account Managers, and 4 SEs) supports both software and services.  Sales offices are in Dallas, Chicago, New York, Boston, Washington D.C., San Francisco and Los Angeles.  The U.S. Sales force will grow to 15 this year.  The European sales force was started in December ’97 with a staff of 6 that will grow to 20 this year.
There are currently 51 customers including The Chicago Tribune, Time Warner’s Pathfinder, NIKE, and National Semiconductor.
	BroadVision Confidential

Vignette Competitive Brief	 PAGE 5	April 1998



