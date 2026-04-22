---
date: 2026-04-22
type: raw
source: /Users/gclyle/mnt/nas-archive/Work/Clients/KROGER/Max Replacement Appriss follow-up.docx
tags: [secure, secure, kroger, retail, client-implementation]
project: secure
status: unprocessed
---

# Max Replacement Appriss follow-up.docx

## Source
File: `/Users/gclyle/mnt/nas-archive/Work/Clients/KROGER/Max Replacement Appriss follow-up.docx`
Size: 6,715 bytes

## Raw content
**Max Replacement**

*Appriss Retail bid follow-up discussion*

Attendees: Don Boyle, John Teller, AJ Crawford, Travis McGuire, Glenn Campbell, Nicholas Creech, Kevin Larson, Chris McCarrick

Appriss: Bob Walters, Geoff Lyle,

Approach: Take us through a simple scenario. Let’s assume replacement of the current, as-is; G-Store T-log file monitoring/self-hosted approach…..and let’s first make sure we understand your pricing…

**Pricing**

1. So we sign your SOW
   - what does this SOW look like?
    Enterprise agreement, w/no limitations on the number of end users, data sources, size of data, etc.? Does annual subscription increase year over year?
   We appreciate your bid including:
   - Dedicated person assigned to the account
   - 3rd line 24/7 help desk support included
   - Integration to LPMS
   - 100 hrs. of report consultation
   - 2-3 day training workshop at client location
2. List price for POS T-log is 1st year annual subscription of $660K & install of $450K
   -again staying with the self-host model, what is the self-hosted pricing for DSD, Pharmacy and e-Commerce?
3. Does Appriss charge Kroger for the Test and Stage environments?
4. Suppose the Kroger phase 1 go-live includes POS T-Logs, DSD, Pharmacy and e-Commerce – what is the subscription and installation cost?
5. If we elected a phased approach, we would be faced with your post-install pricing: DSD @ $350K, Pharmacy@ $ 500K and e-Commerce @ $???
6. Another pricing item requiring further discussion is your offer for an up-front payment / bundled price option. I suggest we put this on the parking lot and come back to it after we have continued going through the self-hosted discussion.

**Functionality**

1. Compatibility with Siteminder? I believe this is Siteminder Enterprise Identity Management (SSO), we currently support Azure AD, ADFS, SAML 2.0, OPEN ID, if I understand Siteminder correctly a provider could be integrated into our SAML 2.0 framework to provide authentication services
2. Ability to save reports to a specific location, yes each user has their own private folders, and shared folders where questions / queries can be saved. Reports are data driven SSRS reports that can be downloaded and saved externally from the application
3. Complete Admin control of application and installation, yes a system administrator can be trained to manage the application
4. Ability to identify and notify inactive users after X amount of days (L) – Not be default, something could be added, may be part of the Siteminder functionality?
5. Ability to notify and delete inactive users after X+Y days (L) – If SSO is configured inactive users are denied entry via the authentication service

**Installation**

1. We understand the self-hosted model typically involves a 20- weeks install after execution of agreement
   Can you provide the WBS for self-host like Chris D'Amore did for SaaS? The tasks in the Plan for Self host vs SaaS are largely the same for POS, when we kickoff we will work with your IT Group to understand the internal project Methodology, dependencies, governance and timeframes for key deliverables such as Hardware and Sales Data feeds. These will drive the implementation schedule and we work out a mutually agreed plan based on a common understanding of the scope of POS EBR. See the attached draft plan that aligns to a 20 week implementation for POS only, this makes some assumptions that hardware and data sources are going to be readily available and per the question below on hardware we have done advance work to size and procure what is required. The Plan for DSD, RX, e-comm and other components that may be brought into scope needs to be mutually agreed, and would be in addition to anything included in the draft plan provided.
   Can any of this work happen now to determine project estimates? Your work breakdown includes capacity planning exercise / develop H/W specs – we need to request funding prior to vendor selection, yes this can be done and expedited. We have completed a preliminary architecture for POS, we would need to do a capacity planning exercise for DSD, RX, etc. to scope out the full extent of the architecture.
2. What is the current delay for a self-hosted customer to receive application releases (SaaS vs. self -hosted)? The software is available on the same schedule, implementation assistance would need to be scheduled and contracted.

**Hardware**

1. The current architecture has several servers to perform the ETL function. We require your assistance in determining the anticipated server count. Do we use the number of transactions, stores or users? The number of load servers would be dependent on the transaction volume, and format of the source data (trickle, daily, by store, all stores) and anticipated peak demand.
2. Does Kroger need to develop the load balancing around these servers? No, we provide that as part of our integration services
3. Is there duplicate checking included in the processing of data? Yes, duplicates are managed in the ETL process
4. Are there any “health check” functions provided to ensure proper loading /processing? Yes, we have a standard load mechanism that has error handling and retry logic built into the process. This is customized based on the source data frequency and format, but works within our framework and can be integrated with third party monitoring services.
5. In post-bid emails, you list 7 weeks of data retention. Kroger will require far more than that. What is maximum retention? Our current sizing estimate estimates a main data repository of ~4TB. We are recommending a physical architecture based on our experience with Retailers of similar size who need to see detailed transactional data for all stores ins a single location. There are many configuration options that could be investigated to provide longer retention periods, and data aggregation strategies to hold key performance / operational metrics at a higher level. We need to understand more about your specific business requirements, IT Infrastructure policies / governance to determine the best configuration that fits within Kroger’s environment and meet functional needs.
6. Is the Appriss solution compatible with Pivotal Cloud Foundry? (Cloud friendly / Cloud Tile) See above, This may be possible, but our initial self-host recommendation is for Physical Hardware due to the size and volume of data in the Kroger estate.
7. Does Appriss provide the optimal database configurations to support the application? (Indexes, views, stored procedures, etc..) Yes, these are delivered out of the box and then via consultancy service they are tuned and indexes added based on specific Kroger db configuration

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
