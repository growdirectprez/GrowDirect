Tractor Supply Reference Call
Sanjay Zachariah
Tuesday December 2nd, 2003
4pm

Went live with SAP in Feb 1999
Initial project began in March 98, 11 months to implement
Implemented IS Retail, FI/CO and WMS
Currently have 4 DC’s – biggest one outside on Indianapolis 500,000 square feet, Waco 300,000 square feet, Omaha Nebraska 150,000 square feet, relocating DC to Atlanta 300,000 sq feet
Another DC planned for next year
Initial release 4.0b of SAP
Early Adopter, first retailer in North America to go live
Upgraded to 4.6 in October 2001
3 months to upgrade., but went through an evaluation process starting in March 2001 to see if it was worth to upgrade, decided to upgrade in June and began implementation in July
4.0 required a lot of OSS notes for bugs, SAP would put out hot packs – combination of OSS notes
Put in hot packs 4 times between 12/99 and 05/01
In 4.6c have not applied any hot packs.  Would like to be current but haven’t seen a need to apply the hot pack
Not a lot of bugs in 4.6c
4.6 met functionality in some areas but some gaps still existed (50-60% of functionality was there, did co-development with SAP to close gaps that existed).  In January will go live with closing most of the gaps
A lot of co-development will go into SAP core 
Identified 21-22 gaps (some big, some small)
Merchandising side, pricing and promotions was a gap, looking for a work bench to do merchandise analysis, this was a gap with SAP
Do a lot of promotions, this was a gap 
What-if analysis was a gap
Currently doing forecasting outside of SAP, an area that SAP is lacking, currently partnering with SAF from Switzerland that will bridge the gap
Store replenishment is forecast for days of supply and arrive at a reorder point, max stock – SAP replenishment takes it from there
All netting and replenishment performed by SAP
For DC’s, demand for all stores is rolled up to the DC level to get demand, determine reorder point and max stock, loaded into SAP
Issues faced were because they were early adopters
A fair amount of bugs
No knowledge base, consultants did not IS-Retail at that time
A lot of trial and error
SAP classes were the first set of courses available
No existing customers to talk to
Data conversion, taking days and weeks to convert the data
Today there is much more knowledge out there
Biggest functionality gaps were in the merchandising area
Finance, warehouse processes are similar to manufacturing thus very few gaps there
Mass maintenance was a gap, no tools available to mass maintain parameters
50,000 SKUs (15,000 inactive, 30,000-35,000active)
450 stores
With 4.6, a lot of mass maintenance capabilities are built in
Ask SAP how do you maintain values, how easy is it to maintain values
Have built “z programs” to help with mass maintenance
Did a lot of development on allocations – push from DCs, push based on historical sales, % of sales, was not easily done in 4.0
In 4.6 allocations are built into SAP
Pay more emphasis on merchandising side when evaluating SAP
Implemented RF with 4.6c in the DCs using SAP WMS
SAP WMS is very close to best of breed
All rebate programs and volume discounts are managed outside of SAP
Extract data from SAP to data warehouse and calculate volume discounts there
Had own data warehouse when implemented 4.0b, still using it, have not implemented BW
If you do volume rebates in SAP, do it in the business warehouse
Accounting used to be Peoplesoft
Merchandising used to be customized JDA (50% JDA and 50% custom)
Had a Y2K issue
Did not want to replace Peoplesoft
Looked at Retek and SAP, decision was made to go with SAP
Biggest advantage of SAP is integration
No sense to integrate Peoplesoft financials with IS-Retail, so implemented SAP financials
Went with a big bang approach
If you do FI first, a lot of throw away interfaces have to be built
FI is a much more stable product than IS-Retail
Implementing FI first helps you get your feet wet with SAP
Believes that Big Bang is much better implementation approach
Change management issues – did not do a lot of change management before the implementation
If they had to do it again, more focus on change management, set expectations right
After demos, believe that it can solve all your problems, need to set realistic expectations
Using home grown POS, does not have perpetual inventory
POS interfaced with home grown sales audit
Use IBM Retail Interchange to map data from sales audit to SAP
At end of each day sales, inventory data extracted to data warehouse
POS has visibility into data warehouse for inventory data
Used to have perpetual inventory in SAP but moved it to data warehouse for better performance
Running on Oracle NT platform
IBM 8 way server for database
7 App servers
Send summary sales data to main SAP system not detailed transactions – this improves performance
Detailed information is managed in data warehouse
No sense in operational SAP system having detailed transaction data
Evaluate sizing for data storage – did not have adequate data storage – have an archiving strategy in place when you go live
Data was populated in tables that was not needed – example in cost center and profit center accounting, detailed data was being populated even though only summary information was required
SAP chosen because SAP is a leader in software applications, one of the concerns they had was financial viability of software vendors – knew SAP would be around for a long time
Did not look at JDA during the selection because the users were not happy with JDA
JDA has progressed quite a bit since then but it is still a bunch of independent systems
Integration benefits of SAP reduces Total Cost of Ownership
Have 3 ABAPers in-house
The advancements that SAP has made in the retail area in the last 3 years are significant.  They have closed the gap by so much.  R&D commitment to retail is huge.
Initial issue that retail product development was determined in Germany, not North American specific – Have moved to a more North American focus recently
As far as SAP retail is concerned, North America has to be a focus because it is the biggest market
Think SAP will be ahead of all the competition in the next 2 to 3 years
Pay attention to reporting requirements.  SAP has 100’s of reports but not exactly what the user is looking for – more information than the user needs – had a process to evaluate the reports to make them specific to Tractor Supply’s needs
Crystal reports can be interfaced with SAP
Just evaluated Crystal, bought Business Objects as a reporting tool for data warehouse and for SAP
