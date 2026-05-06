		









`


TOM Integration

Interface Specification
Item-Region data
From IDS to GFO


[J0052]






Project BEN Code:
W60416
Author:Nitin SinghaiDate:
07/12/2006
Version:
0.2
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:
Sankar G
Reviewed By:
Sankar G

Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc153254735 \h 3
1.1	Purpose of Document	 PAGEREF _Toc153254736 \h 3
1.2	Background	 PAGEREF _Toc153254737 \h 3
1.3	Scope	 PAGEREF _Toc153254738 \h 3
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc153254739 \h 4
2.1	Description of the End-to-End Interface	 PAGEREF _Toc153254740 \h 4
2.2	Requirements for the End-to-End Interface	 PAGEREF _Toc153254741 \h 4
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc153254742 \h 5
3.1	Scope	 PAGEREF _Toc153254743 \h 5
3.2	Source Message Schema	 PAGEREF _Toc153254744 \h 5
3.3	Message Transport Details	 PAGEREF _Toc153254745 \h 5
3.4	Environment and Security Context	 PAGEREF _Toc153254746 \h 5
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc153254747 \h 6
4.1	Scope	 PAGEREF _Toc153254748 \h 6
4.2	Data Validation	 PAGEREF _Toc153254749 \h 6
4.3	Filtering	 PAGEREF _Toc153254750 \h 6
4.4	Mapping	 PAGEREF _Toc153254751 \h 6
4.5	Target Message Schema	 PAGEREF _Toc153254752 \h 10
4.6	Message Transport Details	 PAGEREF _Toc153254753 \h 12
4.7	Environment and Security Context	 PAGEREF _Toc153254754 \h 12
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc153254755 \h 13
5.1	Scope	 PAGEREF _Toc153254756 \h 13
5.2	Data Validation	 PAGEREF _Toc153254757 \h 13
5.3	Filtering	 PAGEREF _Toc153254758 \h 13
5.4	Mapping	 PAGEREF _Toc153254759 \h 13
5.5	Target Message Schema	 PAGEREF _Toc153254760 \h 13
5.6	Message Transport Details	 PAGEREF _Toc153254761 \h 13
5.7	Environment and Security Context	 PAGEREF _Toc153254762 \h 13
6	Testing Deliverables	 PAGEREF _Toc153254763 \h 14
7	Deployment	 PAGEREF _Toc153254764 \h 15
8	Assumptions and Outstanding Issues	 PAGEREF _Toc153254765 \h 16
8.1	Assumptions	 PAGEREF _Toc153254766 \h 16
8.2	Outstanding Issues	 PAGEREF _Toc153254767 \h 16
Appendix A Volumes	 PAGEREF _Toc153254768 \h 17
Appendix B Glossary	 PAGEREF _Toc153254769 \h 18
Appendix C Document Control	 PAGEREF _Toc153254770 \h 19

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t the Item -Region data between Integration Data Store (IDS) and Global Forecasting System (GFO).	
Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including ORMS and GFO. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer business specific Item -Region data from IDS into GFO systems.
Scope
The Interface Specification covers:

audit requirements across the interface
security requirements across the interface
timing/frequency requirements or constraints
support requirements
archiving
the data format to be used for the interface at each stage (e.g. xml messages)
the normal processing required at each stage
recovery from failure required at each stage
volumes.

Note that it is Tesco strategy to avoid placing any business logic in integration layer processing.
Description and Requirements for the End-to-End Interface
Description of the End-to-End Interface
The interface is a batch extract of Item-Region data from an Integration Data Store and upload into the GFO system via integration layer. 
The interface is meant to run at a pre-configured time, which on completion is expected to produce a flat-file (containing reference data records) onto the shared location. This shared location would be monitored by GFO system during specific hours. Once the file containing the extracted data appears on the shared location it should load the data (updates/inserts) into GFO.
Requirements for the End-to-End Interface

Audit Requirements
Each and every interface run should be audited/logged for the purpose of traceability
Security Requirements
The interface executes within a secure private domain. No additional security considerations are required
Timing/Cut-off Constraints
As of now there is no such requirement, however this needs to be re-visited
Performance Requirements
The performance requirements, are unknown at this point of time
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
There is no such requirement
Operational Support Requirements
The due start time and due delivery time of this interface must be defined as IMOF events. These events will be monitored. Alerts will be generated should the interface fail to start, fail to deliver, or deliver late.
The details regarding restart/recovery will be provided after discussion with the GFO team.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Requirements
Although multi-byte character set support is not required for US or Turkey, the interface will support multi-byte character sets through integration
Legal Requirements
There is no such requirement
Compliance To Standards Requirements
To be filled in !!
Processing required in an Extract-Stage of the interface
Scope
A scheduled batch job/s runs, at a pre-configured time, to extract the Item-Region data from the Integration Data Store (IDS). This batch job in turn kicks off a process that executes SQL server Integration Service packages and calls the common forms associated with IDS. After executing the common form service, a complete unload of required data set will be returned as input for the SSIS package. The retuned data-set will be captured and also be transformed into the required format within SSIS package. Batch job should generate the COBOL copy book file which is required for GFO and copy it to the pre-configured share location. The SSIS package will put an exclusive lock to the file until the file creation is complete. As part of data-conversion an extract should convert numeric data to the packed decimal format as per Cobol Copybook format.
Source Message Schema
There is no source message as such. The source data resides in the form of RDBMS tables. The data model diagram will provide necessary information to get the source data. 
Message Transport Details
Feature
Specification
Additional Information
Source System Name
IDS

Source Platform / OS
SQL Server

Source Physical Location


Source Underlying Data Storage Technology
RDBMS

Target System Name
RTI

Target Platform / OS
Windows 2003 Server

Target Physical Location


Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	

Data Format.
XML			
Delimited		
Positional		

Decryption/Encryption
No

Decompression/Compression
No

Transmission Mode
Synchronous		
Asynchronous		
Bulk Data		

Real-time/Scheduled Batch
Scheduled Batch

Archiving
There is no requirement to archive the messages.

Logging
Logging should occur, such that the message can be recreated if necessary.

Error Handling
If the message cannot be delivered, retry 6 times at 10 minute intervals, then raise alert.

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.

Environment and Security Context
Processing required in the Messaging Stage of the interface
Scope
Shipping Agent monitors the file in the configured location for every new file and submits the same to the remote UNIX –AIX share via FTP.
Data Validation
There is no data validations requirement.
Filtering
There is no filtering requirement.
Mapping
Division <-> Department <-> Section -> Class -> Sub-class -> StyleItemLevel1 <-> SKUItemLevel2

Source Data Item
Target Data Item
Comments
Header Record
 
 
 
JLBOA-REC-TYPE
Record type (‘0’ for Header)
 
JLBOA-DATE
Current date when file created. CCYY-MM-DD format.
Set to spaces
FILLER
Set to spaces
 
 
 
Detail Record

 
 
JLBOB-REC-TYPE
Record type (‘1’ for Detail)
SKUItemLevel2  ->> ItemNo
JLBOB-BASE-PRODUCT-NO
Base product number
 
JLBOB-BPR-REGN
Country code.  In the UK this either 'UK' or 'ROI’.  This relates to how data is split between UK and ROI.  The situation in the UK is that a product can exist in both the UK and ROI but some fields can have different values between the 2 counties.  For international we don’t intend to deal with multiple countries (at the moment anyway). 

Therefore this field will be supplied as SPACES and CR will default it.
 
JLBOB-BASE-PROD-RNGE-CLASS
Range class for the product.  Not relevant for International so supply SPACES.
 
JLBOB-BPR-METRO-RCLASS
Metro range class for the product  Not relevant for International so supply SPACES.
 
JLBOB-STORE-ORDERABLE-IND
Store orderable indicator.  This indicator is used to destock and then restock store/products automatically.  It tends to get used where there is a long term out of stock at a DC.  There has been suggestion that this should be supplied by range.  This is something supplied by NBS; do you know where this is obtained from?

CR will probably default this field to 'Y'.

The SRCE-TYPE-IND is used in this processing.

Set to SPACE
 
JLBOB-DEVELOPMENT-LINE
Development line.  UK CR currently picks up 'Y' or 'N'.  CR will default to 'N', but I suspect this could well be a field that may need to be manually overridden for certain products.

Set to SPACE.
 
JLBOB-DIAMOND-PROD-IND
Diamond product.    Currently supplied by NBS as a space and then set to 'N' in CR. 
Set to SPACE.
 
JLBOB-SRCE-TYPE-IND
Source type indicator.    UK CR picks up the following: W - Warehouse, D - Direct, B - Both  Where the indicator is 'B' or 'D' than additional processing is applied to the store orderable indicator to check the product is still orderable indicator to check the product is still orderable from a direct (a check is made against the CR BTS table that holds supplier/TPND data).  CR will probably default to 'B'.

Set to SPACE.
 
JLBOB-ORDER-GROUP
Order Group.    Should be available as a UDA in RMS.  This solution has still not been worked out so for time being set to SPACES
 
JLBOB-RMS-COMM-HIER
The RMS commercial hierarchy.  This is the equivalent of the CR Sub group code.  It is a 20 character string split into 5 fields as follows.  CR will translate this into the appropriate CR 5 character Subgroup code.
Division - >>Division
JLBOB-RMS-DIVISION
RMS Division for this product.  Equivalent to the UK Division.  Supply as a number with leading zeroes.  
Department - >>Department
JLBOB-RMS-GROUP
RMS Group for this product.  Equivalent to the UK Department.  Supply as a number with leading zeroes.  
Section - >>Section
JLBOB-RMS-DEPT
RMS Department for this product.  Equivalent to the UK Section.  Supply as a number with leading zeroes.  
Class - >>Class
JLBOB-RMS-CLASS
RMS Class for this product.  Equivalent to the UK Product Group.  Supply as a number with leading zeroes.  
SubClass - >>SubClass
JLBOB-RMS-SUBCLASS
RMS Sub Class for this product.  Equivalent to the UK Sub Group.  Supply as a number with leading zeroes.  
SKUItemLevel2  ->> ITEM_desc
JLBOB-BASE-PROD-DESCRIPTION
Product description
if(SKUItemLevel2 ->> Standard_UOM)== "EA" then "I" else "W"
JLBOB-SELL-WT-ITEM-IND
Sell by weight indicator.  Currently assumed to be:  I - Item S - Single P - Sell by Pack W - Sell by Weight B - Bird  The main logic in CR doesn’t appear to differentiate between Item and Single.  Some specific B logic does exist. Seperate Pack and Weight logic does exist
 
JLBOB-SALEABLE-EFF-DATE
Sale start date (format ccyy-mm-dd).  CR does use this date in a PFS Sales Extract and as a display field in the online Product mainteneance screen.  The PFS Sales extract doesn't appear to be impacted by removing the Sale Start Date.   Set to SPACES.   
if(SKUItemLevel2 ->> Standard_UOM)== "EA" then "SNGL" else Standard_UOM
JLBOB-S-B-W-UNIT-MEASURE
Sell by weight units.  Currently the only values supplied to CR are: SNGL or KG.  CR appears to only check for a specific value of 'KG'.  For Sell by EACH set to 'SNGL'.   For Sell by Weight, For TURKEY - Set to 'KG', For USA - Set to 'LB'  The product maintenance process in CR will be changed to reference a system wide parameter that identifies the mode that CR will run in (i.e. LB or KG).  Deli counter products (such as Scotch eggs) are currently handled by the sales program that divides the value of products in the bag by the selling price to obtain a number of singles.  This type of processing will be handled by Storeline in TOM. 

JLBOB-UNIT-SIZE      
The unit size of the preferred TPND in the format displayed by CR screens, i.e.  For sale by weight items this field holds the case weight For sell by pack this field holds the contained quantity For all other products it is the unit size  It seems there is not a concept of preferred TPND in RMS.  If this is the case, then use the first active TPND for the TPNB that is found in RMS.  This data item is used as a default in the event that a store specific TPND is not known (based on the supplying stock centre/supplier). 

Note - For Turkey the case weight will be in 'KG's.  For USA it will be in 'LB's (and decimal places of a LB - not ounces).
 
JLBOB-LOW-LEVEL-GRP-CD
Data Dictionary Description: The low level group code is used to group "like" base products within the subgroup for reporting purposes. the definition of "like" will vary from subgroup to subgroup depending on the nature of the products within the subgroup and the reporting requirements.

Set to SPACES.
 
JLBOB-BASE-PROD-SEQ-NO
Data Dictionary Description: A Number to sequence base products within their base product grouping. the sequence will be determined by the reporting requirements.

Set to SPACES.
 
JLBOB-DGRP-CODE
This data item is reliant on the supply authority solution.  
 Data Dictionary Description: A nationally defined group containing one or more base products which will be supplied to any given store from a single source of supply.  

Assume to set as SPACES.
 
JLBOB-MERCH-GRP-CODE
Merchandising code.  Also known as Display Group in International Range.  Set to SPACES
 
JLBOB-SUPP-MERCHG-GRP-CODE
Alternative merchandising code - (for Metro stores)  Set to SPACES
 
JLBOB-MIN-SHELF-LIFE
Minimum shelf life.  If the minimum shelf life is zero and all daily expected shelf live values are zero, then set this field to 999, otherwise set to the minimum shelf life.  Not known at this stage so set to SPACES for time being.  Will need to be resolved longer term.
 
JLBOB-EXPCTD-SHELF-LIFE-1
Day 1 Expected Shelf Life  Not known at this stage so set to SPACES for time being.  Will need to be resolved longer term. Same applies to the other days.
 
JLBOB-DELY-AVAILABLE-IND-1
Day 1 Delivery available indicator.  CR assumes a value of 'Y' or 'N'.  NBS logic says If ‘X’ set to ‘N’ otherwise set to ‘Y’.  CR will probably default to 'Y'. 

Set to SPACE
 
JLBOB-EXPCTD-SHELF-LIFE-2
Day 2 Expected Shelf Life

Set to SPACE
 
JLBOB-DELY-AVAILABLE-IND-2
Day 2 Delivery available indicator.  CR assumes a value of 'Y' or 'N'.  NBS logic says If ‘X’ set to ‘N’ otherwise set to ‘Y’.  CR will probably default to 'Y'.

Set to SPACE
 
JLBOB-EXPCTD-SHELF-LIFE-3
Day 3 Expected Shelf Life

Set to SPACE
 
JLBOB-DELY-AVAILABLE-IND-3
Day 3 Delivery available indicator.  CR assumes a value of 'Y' or 'N'.  NBS logic says If ‘X’ set to ‘N’ otherwise set to ‘Y’.  CR will probably default to 'Y'.

Set to SPACE
 
JLBOB-EXPCTD-SHELF-LIFE-4
Day 4 Expected Shelf Life

Set to SPACE
 
JLBOB-DELY-AVAILABLE-IND-4
Day 4 Delivery available indicator.  CR assumes a value of 'Y' or 'N'.  NBS logic says If ‘X’ set to ‘N’ otherwise set to ‘Y’.  CR will probably default to 'Y'.

Set to SPACE
 
JLBOB-EXPCTD-SHELF-LIFE-5
Day 5 Expected Shelf Life

Set to SPACE
 
JLBOB-DELY-AVAILABLE-IND-5
Day 5 Delivery available indicator.  CR assumes a value of 'Y' or 'N'.  NBS logic says If ‘X’ set to ‘N’ otherwise set to ‘Y’.  CR will probably default to 'Y'.

Set to SPACE
 
JLBOB-EXPCTD-SHELF-LIFE-6
Day 6 Expected Shelf Life

Set to SPACE
 
JLBOB-DELY-AVAILABLE-IND-6
Day 6 Delivery available indicator.  CR assumes a value of 'Y' or 'N'.  NBS logic says If ‘X’ set to ‘N’ otherwise set to ‘Y’.  CR will probably default to 'Y'.

Set to SPACE
 
JLBOB-EXPCTD-SHELF-LIFE-7
Day 7 Expected Shelf Life

Set to SPACE
 
JLBOB-DELY-AVAILABLE-IND-7
Day 7 Delivery available indicator.  CR assumes a value of 'Y' or 'N'.  NBS logic says If ‘X’ set to ‘N’ otherwise set to ‘Y’.

Set to SPACE
 
JLBOB-DIR-ORD-GRP
Directs order group  In UK this field is usually 'Z' except for bakery products that are not in scope for International.  CR will default this field to 'Z'.

Set to SPACES
 
JLBOB-NOM-PACK-WEIGHT
Nominal pack weight of the preferred TPND.  If  SELL_BY_WGT_ITEM_IND != ‘P’  set NOM-PACK-WEIGHT to zero otherwise  Calculate NOM-PACK-WEIGHT as CASE WEIGHT divided by CONTAINMENT QTY  It seems there is not a concept of preferred TPND in RMS.  If this is the case, then use the first active TPND for the TPNB that is found in RMS.  This data item is used as a default in the event that a store specific TPND is not known (based on the supplying stock centre/supplier).   Note - For Turkey this will be in 'KG's.  For USA it will be in 'LB's (and decimal places of a LB - not ounces).   Not known at this stage so set to ZEROES for time being.  Will need to be resolved longer term.
 
JLBOB-TU-NOTIONAL-WT
Notional case weight of the preferred TPND.  If none exists set to zero.  It seems there is not a concept of preferred TPND in RMS.  If this is the case, then use the first active TPND for the TPNB that is found in RMS.  This data item is used as a default in the event that a store specific TPND is not known (based on the supplying stock centre/supplier).   Note - For Turkey this will be in 'KG's.  For USA it will be in 'LB's (and decimal places of a LB - not ounces).    Not known at this stage so set to ZEROES for time being.  Will need to be resolved longer term.
 
 
 
Trailer Record

 
 
JLBOZ-REC-TYPE
Record type (‘9’ for Trailer)
 
JLBOZ-REC-COUNT
Record count including the header and trailer records.
 
FILLER
 

Target Message Schema
Field NameReferenced in CR?Insync formatStartLengthCOBOL Format





Header Record
(needs to exist)
G
1
170
 
JLBOA-REC-TYPE
Y
C 1
1
1
X
JLBOA-DATE
Y
C 10
2
10
X(10)
FILLER
N
C 159
12
159
X(159)
 
 
 
 
 
 
Detail Record
(needs to exist)
G
1
170
 
JLBOB-REC-TYPE
Y
C 1
1
1
X
JLBOB-BASE-PRODUCT-NO
Y
Z 9
2
9
9(9)
JLBOB-BPR-REGN
Y
C 2
11
2
X(2)
JLBOB-BASE-PROD-RNGE-CLASS
Y
C 2
13
2
X(2)
JLBOB-BPR-METRO-RCLASS
Y
C 2
15
2
X(2)
JLBOB-STORE-ORDERABLE-IND
Y
C 1
17
1
X
JLBOB-DEVELOPMENT-LINE
Y
C 1
18
1
X
JLBOB-DIAMOND-PROD-IND
Y
C 1
19
1
X
JLBOB-SRCE-TYPE-IND
Y
C 1
20
1
X
JLBOB-ORDER-GROUP
Y
C 2
21
2
X(2)
JLBOB-RMS-COMM-HIER
Y
G
23
20
 
JLBOB-RMS-DIVISION
Y
Z 4
23
4
9(4)
JLBOB-RMS-GROUP
Y
Z 4
27
4
9(4)
JLBOB-RMS-DEPT
Y
Z 4
31
4
9(4)
JLBOB-RMS-CLASS
Y
Z 4
35
4
9(4)
JLBOB-RMS-SUBCLASS
Y
Z 4
39
4
9(4)
JLBOB-BASE-PROD-DESCRIPTION
Y
C 48
43
48
X(48)
JLBOB-SELL-WT-ITEM-IND
Y
C 1
91
1
X
JLBOB-SALEABLE-EFF-DATE
Y
C 10
92
10
X(10)
JLBOB-S-B-W-UNIT-MEASURE
Y
C 4
102
4
X(4)
JLBOB-UNIT-SIZE      
Y
Z 5, 2
106
7
9(5)V99
JLBOB-LOW-LEVEL-GRP-CD
Y
C 2
113
2
X(2)
JLBOB-BASE-PROD-SEQ-NO
Y
C 3
115
3
X(3)
JLBOB-DGRP-CODE
Y
C 3
118
3
X(3)
JLBOB-MERCH-GRP-CODE
Y
C 3
121
3
X(3)
JLBOB-SUPP-MERCHG-GRP-CODE
Y
C 3
124
3
X(3)
JLBOB-MIN-SHELF-LIFE
Y
Z 3
127
3
9(3)
JLBOB-EXPCTD-SHELF-LIFE-1
Y
Z 3
130
3
9(3)
JLBOB-DELY-AVAILABLE-IND-1
Y
C 1
133
1
X
JLBOB-EXPCTD-SHELF-LIFE-2
Y
Z 3
134
3
9(3)
JLBOB-DELY-AVAILABLE-IND-2
Y
C 1
137
1
X
JLBOB-EXPCTD-SHELF-LIFE-3
Y
Z 3
138
3
9(3)
JLBOB-DELY-AVAILABLE-IND-3
Y
C 1
141
1
X
JLBOB-EXPCTD-SHELF-LIFE-4
Y
Z 3
142
3
9(3)
JLBOB-DELY-AVAILABLE-IND-4
Y
C 1
145
1
X
JLBOB-EXPCTD-SHELF-LIFE-5
Y
Z 3
146
3
9(3)
JLBOB-DELY-AVAILABLE-IND-5
Y
C 1
149
1
X
JLBOB-EXPCTD-SHELF-LIFE-6
Y
Z 3
150
3
9(3)
JLBOB-DELY-AVAILABLE-IND-6
Y
C 1
153
1
X
JLBOB-EXPCTD-SHELF-LIFE-7
Y
Z 3
154
3
9(3)
JLBOB-DELY-AVAILABLE-IND-7
Y
C 1
157
1
X
JLBOB-DIR-ORD-GRP
Y
C 2
158
2
X(2)
JLBOB-NOM-PACK-WEIGHT
Y
Z 3,2
160
5
9(3)V99
JLBOB-TU-NOTIONAL-WT
Y
Z 4,2
165
6
9(4)V99
 
 
 
 
 
 
Trailer Record
(needs to exist)
 
 
 
 
JLBOZ-REC-TYPE
Y
C 1
1
1
X
JLBOZ-REC-COUNT
Y
Z 8
2
8
9(8)
FILLER
N
C 161
10
161
X(161)


Message Transport Details 
For messages destined for TO system, the following applies.	

Feature
Specification
Additional Information
Source System Name
RTI

Source Platform / OS
WOF

Source Physical Location


Source Underlying Data Storage Technology
File System

Target System Name
CR

Target Platform / OS
UNIX –AIX

Target Physical Location


Target Underlying Data Storage Technology


Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		

Data Format

XML  				
Delimited 			
Positional 			

Decryption/Encryption
No

Decompression/Compression
No

Transmission Mode
Synchronous 			
Asynchronous 			
Bulk Data 			

Real-time/Scheduled Batch
Real-time

Archiving
There is no archiving requirement

Logging
Should logs be kept of all actions? For how long should these be stored?
Logging should occur, such that the message can be recreated if necessary.

Error Handling
If the message cannot be delivered, retry 6 times at 10 minute intervals, then raise alert.

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.




Environment and Security Context
Messaging will happen through Shipping Agent. The Real Time Integrator or BizTalk2006 EAI tool will be set with the Environment specification (will be defined)
 

 
Processing required in the <third stage of the interface>
Scope
Not Required

Data Validation
Not Required

Filtering
Not Required

Mapping
Not Required

Target Message Schema
Not Required

Message Transport Details
Not Required

Environment and Security Context
Not Required
Testing Deliverables
Unit Test Scripts
Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1
The messaging task will be started at EOD



Outstanding Issues
ID
Issue
To be addressed by
1
JLBOB-ORDER-GROUP - Method to populate of this field data needs to be identified
Engagement Architect
2
JLBOB-UNIT-SIZE - Method to populate of this field data needs to be identified 
Data Modeller
3
JLBOB-MIN-SHELF-LIFE - Method to populate of this field data needs to be identified
Engagement Architect
4
JLBOB-EXPCTD-SHELF-LIFE - Method to populate of this field data needs to be identified
Engagement Architect
5
JLBOB-NOM-PACK-WEIGHT - Respective field needs to be identified
Data Modeller
6
JLBOB-NOM-PACK-WEIGHT - Method to populate of this field data needs to be identified
Engagement Architect
7
JLBOB-TU-NOTIONAL-WT - Method to populate of this field data needs to be identified
Engagement Architect


Volumes
Glossary

Acronym
Term
Description
EAI
Enterprise Application Integration
The process of meeting the data requirements of applications by providing a message based transport from disparate data sources across all forms of enterprise technology.
EAI Layer
Enterprise Application Integration Layer
Refers to the integration services provided to implement EAI. In contrast to the EIA Layer for data services. See below.
EIA
Enterprise Information Architecture
Creation of a strategic single view of data across the enterprise.
HIS
Host Integration Server
A gateway to transferring data between a Mainframe system and another system.

Interface
Many definitions exist for 'interface'. In general, 'interface' refers to the link between a data source and a data target. And there are properties of the interface in this context. However more specifically 'interface' refers to one end of a data link, hence the terms source interface and target interface, and both the source interface and the target interface will have specific properties of their own.
ODS
Operation Data Store
A store of data, logically residing in the EIA layer, that provides an authoritative single view of a discrete data component specific to the enterprise. Eg: Product, Customer, etc. ODS's reside in the EIA Layer, and are accessed through the EAI Layer.
TIB
Tesco Integration Bus
The managed service provided by Tesco's EAI Layer for data transportation and the integration of applications with legacy data sources and Operational Data Stores. 'Larger' in concept than the EAI Layer to include implementation details and interfacing between the EAI (integration services) Layer and the EIA (data services) Layer
WOF
Wintel Operational Framework
The Windows software/Intel hardware environment
->
One to Many Relationship
In a Subject hierarchy the entities defined as parent and child symbolize in this way.
<->
Many to Many Relationship
In a Subject hierarchy the relationship between the entities defined with many to many relationship without relationship table symbolize this way.

Document Control
Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
06-12-2006
V0.1 Draft
First issue
Sankar G
07-12-2006
V0.2 Draft
Second Issue











Related Documents

Author	
Date
Version
Title


















Distribution

Name
Position
Approver/Contributor/Other
Nathan Smith
Enterprise Architect

Adrian Hinks
Engagement Architect

David Onyett
Project Lead






















Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 5 of  NUMPAGES 22	Date:  SAVEDATE \@ "d MMM yyyy" 26 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































