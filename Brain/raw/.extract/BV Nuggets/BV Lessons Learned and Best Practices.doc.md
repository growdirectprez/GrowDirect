BroadVision Lessons Learned and Best Practices

Experiences from a BroadVision implementation


By Christian Saucier, PriceWaterhouseCoopers
christian.saucier@us.pwcglobal.com

12/09/1999


 TOC \o "1-8" BROADVISION LESSONS LEARNED AND BEST PRACTICES	 PAGEREF _TOC473033131 \H 1
EXPERIENCES FROM A BROADVISION IMPLEMENTATION	 PAGEREF _TOC473033132 \H 1
I	ABOUT THIS DOCUMENT	 PAGEREF _TOC473033133 \H 3
II	FRONT-END CONSIDERATIONS	 PAGEREF _TOC473033134 \H 4
1	Frame Usage Impacts	 PAGEREF _Toc473033135 \h 4
1.1	BroadVision With Frames	 PAGEREF _Toc473033136 \h 4
1.2	BroadVision Without Frames	 PAGEREF _Toc473033137 \h 6
2	Doc-Root or Script-Root?	 PAGEREF _Toc473033138 \h 6
3	Choosing a Home for Your Textual Data	 PAGEREF _Toc473033139 \h 7
3.1	Storing Data in the DCC	 PAGEREF _Toc473033140 \h 7
3.2	Storing Data in the File System	 PAGEREF _Toc473033141 \h 8
3.3	Database and External Systems Data	 PAGEREF _Toc473033142 \h 9
4	Visual Elements Model	 PAGEREF _Toc473033143 \h 9
III	DEVELOPING BROADVISION COMPONENTS	 PAGEREF _TOC473033144 \H 10
1	Memory Management	 PAGEREF _Toc473033145 \h 10
2	Minimising Cross-Layer Calls	 PAGEREF _Toc473033146 \h 10
IV	INFRASTRUCTURE CONSIDERATIONS	 PAGEREF _TOC473033147 \H 11
1	Make Use of the Script Library	 PAGEREF _Toc473033148 \h 11
2	Never Re-Use Function Names	 PAGEREF _Toc473033149 \h 11
3	Central Configuration File	 PAGEREF _Toc473033150 \h 12
4	Debugging and Error Handling	 PAGEREF _Toc473033151 \h 12
4.1	Debugging	 PAGEREF _Toc473033152 \h 12
4.2	Error Handling	 PAGEREF _Toc473033153 \h 12
V	ENGINE CONFIGURATION	 PAGEREF _TOC473033154 \H 14
1	Do You Want a Cookie?	 PAGEREF _Toc473033155 \h 14
2	Caching Concerns and Solutions	 PAGEREF _Toc473033156 \h 14
2.1	BroadVision IM Cache	 PAGEREF _Toc473033157 \h 15
2.2	Web Server Cache	 PAGEREF _Toc473033158 \h 15
2.3	Browser Cache	 PAGEREF _Toc473033159 \h 15
2.4	Proxy Cache	 PAGEREF _Toc473033160 \h 16
3	How Many Interaction Managers Do I Need?	 PAGEREF _Toc473033161 \h 16
VI	WORK ORGANIZATION	 PAGEREF _TOC473033162 \H 17
1	How Many IM Engines For Your Developers?	 PAGEREF _Toc473033163 \h 17
2	Promoting the Code	 PAGEREF _Toc473033164 \h 17
VII	YOUR MILEAGE MAY VARY	 PAGEREF _TOC473033165 \H 18
About this Document

This document has been written to share some of the lessons learned in the course of implementing a web site using BroadVision One-to-One version 4.1. It will highlight and give some insights on important questions that will surface during the design and implementation of your application.  In many cases, there is no right or wrong answer and decisions will have to be made on a case-by-case basis however, we hope that the knowledge documented here will help you follow the best path for your environment.  

The methods and techniques that are suggested in this document should be considered complimentary to BroadVision's own recommended best practices.  This document is not endorsed by BroadVision and some opinions and findings may go against BroadVision's own best practices.  In such a case, good judgement and experience will be the best assets to make the appropriate decisions.

Front-end Considerations

Frame Usage Impacts

For better or for worse, the decision to use frames is generally made from a site-wide look & feel perspective and the technical arguments on the matter often take second rank.  This decision (or, in other cases, decree) will impact how BroadVision can be utilized to implement site functionality.   

This document will try to be impartial on the endless argument about frames or no-frames site design.  The use of frames is a decision that must be analysed thoroughly and seriously at the early stages of the design phase.   In some cases, frames make sense.  In other cases, they don't. 

BroadVision With Frames

A frame-based user interface can allow the BroadVision site architect to design a relatively small number of generic templates (the frameset documents) that uses BroadVision's server-side processing capabilities to dynamically select the content of each frame based on logic or results obtained from DCC rules resolution. The template scripts provides a layer of control that can oversee a number of screens of a similar nature and resemblance.  

For example, in a site that offers information based on the user's membership level, a controlling "user information" template can decide if a user is going to be presented with the standard or premium version of a screen. The controlling template could extract the user profile from the DCC and decide at processing time which of the screens to display in the target frame.

This allows the designer to split screen-level logic from the session handling and user guidance logic.  The templates can thus shield a lot of complexity from the screens themselves and greatly simplify the work of screen designers.  In fact, in such a scenario, many screens will not contain any dynamic information whatsoever and can simply be built using a regular HTML editor.
Dynamic Page Templates

















In  REF _Ref469394341 \r \h Figure  1, static screens (those without server-side BroadVision logic) are showed in pale gray and dynamic screens and templates are showed in dark gray.  The dynamic templates create a frameset document that can select between a number of screens to be sent to the browser.  The arrows represent hypothetical links that could exist between the various screen elements of the site.  Some arrows represent screens jumping to other screens under a parent template and others represent screens jumping to templates that will in turn select the appropriate screens to be displayed in the frames. 

In this environment, a template would be defined as a dynamic HTML frameset that can select amongst a variety of static or dynamic HTML documents to be displayed in its frames.

Site architects have to keep in mind that the use of frames also has some drawbacks; these drawbacks are well known to web designers and users alike.  Amongst others, client-side JavaScript, status messaging between the frames, and the use of the "back" button on the browser, are common sources of headaches in a frame oriented web site.  Another possible problem is that a user could navigate from one static screen to another within a single dynamic frameset long enough without reloading the frameset itself and thus cause the BroadVision session to expire.  Of course, most of these pitfalls can be circumvented with an appropriate design but to do so requires a significant amount of extra efforts.



BroadVision Without Frames

In nearly every site, regardless of your use of frames, there is a need to repeat visual elements (a page header for example) from one screen to another.  (Section  REF _Ref469390186 \w \h II4 on page  PAGEREF _Ref469390186 \h 9 elaborates on the concept of visual elements.) On a frame-less site, the Server-Side Include (SSI) functionality provides the mean to embed such re-usable visual elements within a document.  

However for the purposes of a dynamic screen, this SSI functionality is not as flexible as a frameset document.  The biggest constraint is the fact that the file inclusion is done by a pre-processor and thus, the #include statement cannot contain any dynamic BroadVision variables or statements.

Because of these limitations, it becomes difficult and sometimes cumbersome to use regular HTML creation tools to build frameless dynamic screens.  In all likeliness, a visual HTML editor will not be a good tool for the development of those dynamic screens; the HTML output of such tools is often messy and they cannot properly render the results of server-side logic that must be processed by the BroadVision engines. 

Doc-Root or Script-Root?

The BroadVision Interaction Manager (IM) engines parse every file, regardless of their type or extension, located under the script-root directory.  Obviously, all your jsp scripts should reside under the script-root but a question that may arise is if you should place your static documents in there as well?  In a few cases, BroadVision has recommended placing static documents under the script-root, this recommendation is based on convenience and better caching algorithms than those provided by some web servers.

Our experience raises some significant issues regarding this recommendation and you should consider carefully the following points before making your decision: 
The availability of every static document stored in the script-root is dependent on the availability of the IM engines.
Your static documents cannot coexist in the same tree branch as your binary files (graphics, and others).  The IM will try to parse any binary files in your script-root and cause it to crash and return an error. In some environments, the two branches –script-root and doc-root– can be located on totally different servers (in your production environment, your web servers are likely to be on different machines than your IM servers).
When using  HYPERLINK  \l "Do_You_Want_a_Cookie" cookies to carry session and engine information from one screen to another, the static documents can become unavailable when/if the session expires.

For these reasons (and certainly many others), unless you have a strong justification or a unique and specific requirement, we would recommend against placing your static documents in the script-root directory.

Choosing a Home for Your Textual Data

There are generally three locations where you can store textual content that can be used by your dynamic documents:

 HYPERLINK  \l "Storing_Data_in_the_DCC" The Dynamic Control Centre (DCC)
 HYPERLINK  \l "Storing_Data_in_the_File_System" A file (HTML or other) in the file-system
 HYPERLINK  \l "Database_and_External_Systems_Data" A database or external system

Storing Data in the DCC

BroadVision recommends the use of the DCC over the file system or other mechanisms to store textual site content. The standard BroadVision installation provides many content types that can be used for such purposes (editorials, products and others).  These content types can be extended to meet specific needs and it is also possible to design proprietary content types.

One significant advantage brought by the DCC is the possibility to build generic templates in a  HYPERLINK  \l "BroadVision_Without_Frames" frame-less environment.  In this scenario, most HTML formatting tags would be contained in the templates and the DCC would be only used to store textual elements.  Unlike SSI #include statements that imports file system data at pre-processing time, DCC rules resolution can include DCC data dynamically and JavaScript logic can decide between two different textual data elements to be displayed.

However, using the DCC to store data also brings some complications.  One disadvantage is the difficulty to create and modify the data.  Content designers must use the DCC to edit or add content and the DCC interface is not particularly well suited for HTML content editing.  Integration between DCC and the file system or third party products is badly needed. 

Also noteworthy is the fact that, at the time of writing, the migration tools used to extract and promote DCC data and rules have proven to be unreliable and unsupported by BroadVision. Other DCC related difficulties were reported to BroadVision but dates for the availability of a fix or patch have not yet been provided.  Some of the issues reported are:

The migration tool for DCC data doesn't support rules definition
DCC will not display value pull-down lists for custom content-types

To circumvent some of these problems, you may need to create your own database extraction and population scripts.  BroadVision does not recommend this practice, as it may be difficult to keep the data in sync between all environments.

Storing Data in the File System

A natural location for reports, announcements, editorials and other text-rich documents would be an HTML file in your doc-root directory.  You can build dynamic screen wrappers (with or without frames) that put together the various visual elements of a screen around and along with your HTML documents.

This method allows you to leverage the numerous content creation and versioning tools that are available for your environment.  Content creators are usually more comfortable to use their familiar editor instead of using the DCC to write a document.

However, this solution comes with a price.  In a frame-less environment, you will have to create a dynamic wrapper document for each static HTML document that you want to display.  For example, a whatsnew.jsp wrapper could #include header.jsp, navbar.jsp, whatsnew.html and footer.html.  This could cause some difficulties in large sites where the number of files will grow considerably. (The reason for this is that you would need to create a whatsnew2.jsp to wrap a new whatsnew2.html file.)  The following graphic illustrates this scenario where each section of the overall screen is brought together by using SSI functionality.

Visual Page Elements











 




Database and External Systems Data

In all likeliness, every site will need to access some piece of data that is either too complex to be represented in the DCC, or only available through a legacy application. 

Complex data structures will require their own specific set of data tables. To access these tables from a dynamic script you can use BroadVision's Generic DB Accessor component.  This component supports any of the database vendors that are supported by the One-to-One product itself.  Calls to the Generic DB Accessor can be made while the page is being generated and thus provides a lot of flexibility to present the data to the visitor.  However, BroadVision discourages the use of the Generic DB Accessor because of unspecified performance and scalability issues.  We would suggest that BroadVision needs to perfect their Generic DB Accessor as it is a tool that is likely to be required by many projects.  In-house development of data components should also be considered.

Legacy or external applications can be interfaced with by creating a custom component. This component can wrap an existing API or parse an output file from the legacy/external system.  The component will expose its own interface to the IM engines that will then be allowed to use this functionality to extract data for the dynamic pages.  See section  REF _Ref473032868 \r \h III, on page  PAGEREF _Ref473032902 \h 10 for more details on custom BroadVision components.

Visual Elements Model

As illustrated by  REF _Ref469394439 \n \h Figure  2  REF _Ref469394439 \p \h above, one of the ways to minimize redundancy and keep the number of files under control on your site is to build visual elements that are included in screens by SSI statements or frameset documents.  

Using server-side scripting, you can make your visual elements intelligent enough to understand the context in which they are being called and thus provide the user with the appropriate visual representation.  For example, a dynamic navigation bar element could be contained in a single file and perform the proper highlights and menu item selection as appropriate for the current visitor context.

Developing BroadVision Components

When a server-side script reaches a certain level of complexity or when data must be extracted from an  HYPERLINK  \l "Database_and_External_Systems_Data" external system, it is recommended to create a component that will perform the required functionality. Custom components can currently only be developed in C++; a future release of BroadVision will provide the ability to create components in Java.

Memory Management

The most important and difficult aspect of developing components is the memory management.  The BroadVision IM engines are very sensitive to memory leaks within components.  That is why, the use of RogueWave libraries and Purify software is recommended. The RogueWave libraries simplify the developer's tasks of allocating and releasing memory that is required for strings and other data types required in the component.  It is not necessary to use these libraries to develop a functional component.

BroadVision also recommends the use of a Rational software called Purify. Purify provides detailed reports on application memory usage which can give a developer great insights when trying to identify the location of potential memory leaks.  Purified components should only be used in a development environment; a normal component should be compiled for your production systems.

Minimising Cross-Layer Calls

One aspect to keep in mind when building components for the dynamic documents is to avoid the situation where the script developer will be required to make multiple calls to the component layer in order to accomplish a single task.  We can explain this by looking at a dynamic document as having three layers: 

the HTML layer, 
the server-side JavaScript layer, 
the component layer.  

Performance degradation occurs every time a jump is made from one layer to another. This is not only important for the component developer but also for the script developer.  The script developer should try to minimize the number of "<%" and "%>" as well as the number of calls to components within a dynamic document. 

Minimizing cross-layer calls will ensure that each screen performs adequately, even when put to stress in testing and/or real-life scenarios.
Infrastructure Considerations

Make Use of the Script Library

The script library is a location where developers can place common functions that can be re-used throughout the site.  Make sure that you build and document some basic common functions early in the development process so that screen developers can make use of their functionality at the beginning of their development efforts.

Here are some common functions that you will most likely need to have in your script library:

A script initialization function that gets called at the beginning of every dynamic document.  This will give you a location to put common session-handling or user tracking logic that can affect every screen of your site
A script termination function that gets called at the end of every dynamic document.  Here you might want to put a common footer copyright notice or a server notification confirming the end of a screen transfer to the user.
An error logging function.  This will provide a common mechanism for dynamic documents to log errors to log files, users or system administrators. 
Anything else that you may think of...  In fact, if you think of a function that two screens can benefit from, you should probably put that function in a script library.  You can organize your script library functions in various files and directories so don't be afraid to share your functions with others through this mechanism.

Never Re-Use Function Names

All the dynamic documents share a common set of run-time engines that interpret and output the results of the scripts to the user.  Function declarations are cached within these run-time engines' memory space and subsequent scripts may make use of this cache when they make a call to the same function.  For these reasons, you should make sure that no script tries to re-define a function that was already defined in another script.

Failure to comply with this rule can lead to erratic results where an already cached function will be executed instead of a newly re-defined function of the same name within the script.  To avoid these problems, make sure that you use the script library to share generic functions and make sure that you give meaningful names to your functions so that the risks of someone else creating a function with the same name is minimized.

You should keep a project-wide document that defines all script-level and script library-level functions.  Each developer should keep this document up to date and refer to it on a regular basis.

Central Configuration File

You might want to consider implementing a central configuration file for your site.  This file would contain global configuration settings that could be read by a script on the home page and set into session for each site visitors.   The file is totally independent of any other system or BroadVision configuration files.  It simply provides a central place to easily tweak site-specific settings.

For example, you could set the following settings in this file: 

The administrator's email address
The site's debugging level (see error handling and debugging section)
Default values for various site-specific variables

Debugging and Error Handling

Debugging

As mentioned in section 3.1, your should implement a site-wide error logging function in the script-library that can be called by all the page scripts.  The page scripts should make ample use of the common logging function and log various key variables and milestones with appropriate logging level set for each entry.  

The central configuration file (see section 3.3) could select which level of logging is appropriate for the environment.  Logging levels could range from 0 (log nothing) to 5 (log everything).

Building a streamlined debugging environment like this will prove to be very valuable in troubled times.  Each environment, from development to production, can have a different logging level set in the central configuration file.  In case of emergency, the logging level can be easily raised to better understand the problematic behavior of the site.

Error Handling

There are two error pages that you will want to implement for your site: one is dynamic and the other, static.  

The static error page is a simple HTML file that is displayed to the visitors whenever something goes terribly wrong with either the BroadVision engines, the visitor's session or the page script code.  The static page is specified by the "default-page" entry in the interaction manager configuration file located in the /etc/opt/BVSNsmgr directory.  The static error page must be stored in the document root so that it is not dependent of any dynamic engine.

The dynamic page is not part of BroadVision's standard design but can be a useful tool for gracefully handling unexpected scenarios in page scripts.  Simply put, the page scripts can reference the dynamic error page whenever an undesired and trappable condition occurs.  The dynamic error page can contain some dynamic logic that uses the session and visitor information to guide the visitor towards an appropriate destination.  The dynamic error page can also contain some information (hidden or visible) that indicates the state of some key session variables at that moment.

Engine Configuration

Do You Want a Cookie?

BroadVision supports the use of cookies to carry session and engine information from one page script to another.  Alternatively, the session and engine ids can be passed through the URL string but this makes for some long and cryptic URLs that are not always convenient for search engines and browsers bookmarking purposes. 

As with frames, the decision to use cookies may have some political repercussions and is a constant subject of debate in many forums on the Internet.

If you decide to use cookies on your site, here are some BroadVision specific considerations to keep in mind:

At the beginning of your site, you want to set the cookie on the browser using the Session.autoSetBVCookie(9) function call.   This will set a temporary cookie on the browser that will only be alive while the browser is kept open.  
Be sure that your pages can support the absence of a cookie.  A user could bookmark a page in the middle of your site and might attempt to jump to that page directly at a later date.  Your page must then be able to either handle a sessionless visitor (where none of the expected session or visitor variables are set), create a new session (using the initSessionScript() function call for example), or redirect the visitor to the home page.
The session can expire (if a user is idle too long for example) and, if the browser were kept open, the cookie would still reference the old session. There are no easy ways out of this; make sure that you set the default error page in the IM configuration file if you want to hide the 'invalid session' message from the visitors.  Also consider the use of BV_UseBVCookies query string variable to ignore the cookie value.
You can use the "?BV_UseBVCookies=no" in your query string to tell the BroadVision engine to ignore the cookie information.  This will ignore both valid and invalid cookies and will attempt to run your page script without any session or visitor information.

Caching Concerns and Solutions

Be careful that you don't get fooled by the various caches that are involved in your environment.  

The BroadVision IM engines may keep a cached copy of the files served from the script root. 
The Web server may keep a cached copy of the files from the document root.  
The browser may keep a cached copy of the downloaded pages on your client computer
Any other layers in between, like a proxy server, may also keep a cached copy of the pages

Generally speaking, you will not want to have the caching engines enabled in your development environment or in any environment where the files are changed frequently.  Caching algorithms don't always properly detect that a file has changed and you may get an older cached copy of your file.  You should either disable the caching engines or flush the content of your caches every time you change the content.  Let's look at each caching layer a little more carefully:

BroadVision IM Cache

In your development environment, make sure that you turn off BroadVision's cache unless necessary.  You can turn off the cache by running the cache utility after you've restarted the IM engines.  If you do not turn off the cache (or at least flush it), you may find that a new file that was recently copied in the script root may not show the recent changes when requested by the browser.   
Use the following command to flush the BroadVision cache: 
cache_utl –e script_cache –d flush

Use the following command to disable the BroadVision cache:
cache_utl –e script_cache –d disable

Note: You need to disable the cache every time you restart the IM engines.

Web Server Cache

Keep in mind that your web server could cache a file from the document root.  Refer to your web server documentation to know how to clear or disable the cache for your development environment.

Browser Cache

When it comes to caching, different browsers behave differently.  There are many <meta> statements that instruct the browsers not to use their cache or to expire a cached copy of a document.  However, the reliability of these <meta> statements cannot always be trusted and again, their behavior changes from one browser to another.

The following <meta> statements have proven useful to handle caching issues with most browsers:
<meta http-equiv="Expires" content="0">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="No">

The only sure way to make sure that a page does not get confused with a cached copy is to give each page a unique URL.  URLs to dynamic pages can include key values in the query string to give each rendition of the page as unique a URL as possible.  

Combining the unique URL with the <meta> tags should make your dynamic pages as cache-proof as possible.

Proxy Cache

Another treacherous level of caching is the proxy server cache.  Many ISPs use proxy server caching to reduce the amount of network traffic on their networks.  Most of the time, the only way that a proxy cache has to differentiate between a current and a cached copy of a page is by comparing the URL strings. Refer to section 4.2.3 for more details on unique URLs.

How Many Interaction Managers Do I Need?

The number of IM engines that is required in your higher environments (testing, staging and production) will vary depending on sizing estimates, budget, and available hardware.  Make sure that each IM configuration file properly references the root host and the other IM IP addresses.  Refer to section 5.1 for more suggestions for your development environment.

Work Organization

How Many IM Engines For Your Developers?

Your development environment should be setup with an IM engine for each developer (or at least one IM for each 2 or 3 developers).   This working environment will allow the developers to control (or crash) their IM without affecting the rest of the team.  

You should also consider creating multiple root-hosts and web server instances for the developers' working environment.  Ideally, for your working environments, you want to have a one-to-one relationship between the root-host, the IM, the web server and the developer.  Some organizations even go as far as creating a separate database table space for each developer!

Promoting the Code

Your source control system (cmvc, cvs, vss or others) should allow you to check your files in and out from a central development environment to/from your individual working environments.  Developers can thus test their changes locally in their work environments and then check-in the modified files in the central development environment.

Your Mileage May Vary

Obviously it is impossible to address every scenario and every situation in a document like this.  Different clients will have different environments that may call for different measures.  A strong element of success for your project will be to gather one or two experienced BroadVision resources that can be used as architects and guide for the other developers. 

Also keep in mind that BroadVision is still evolving.  Although it is one of the leading and best tools in its category, it has quite a bit of maturity to gain.  New releases of BroadVision will certainly address some of our concerns and potentially impact many of the recommendations included in this document.








PricewaterhouseCoopers Confidential  PAGE 1 of  NUMPAGES 18


Home

Template 1

Template 2

Screen 1

Screen 2

Screen 3

Screen 4

Screen 5

Template 3

Screen 7

Screen 6

Header.jsp

N a v b a r


Whatsnew.html


Whatsnew2.html



Whatsnew.jsp

Whatsnew2.jsp


 EMBED Word.Picture.8  



