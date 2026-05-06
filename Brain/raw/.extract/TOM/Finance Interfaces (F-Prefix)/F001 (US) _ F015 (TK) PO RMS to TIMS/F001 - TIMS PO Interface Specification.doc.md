		









`


TOM Integration

Interface Specification
Purchase Order data
From RMS to TIMS


[F001]






Project BEN Code:
W60416
Author:Supriyo ChakrabortyDate:
18/12/2006
Version:
0.5
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:

Reviewed By:
Andrew barker

Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
27-Dec-2006
0.1D
Draft
Supriyo Chakraborty
28-Dec-2006
0.2D
Draft
Sankar G
03-Jan-2007
0.3D
Draft
Sankar G
09-Jan-2007
0.4D
Draft
Supriyo Chakraborty
15-Jan-2007
0.5D
Draft
Sankar G
30-Jan-2007
1.0
First Release

Reviewers

Name
Position
Sankar G
Business Analyst
Andrew Barker
Solution Architect




Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Andrew Barker
Position
Engagement Architect
Signature
<Physical signature or via email approval>
Date
dd/mm/yyyy (<version signed off>)

Distribution List

Name
Date of Issue
Version

<Issue Date>
<Version No>










Document Source
Clear Case

Related Documents

Directory: Operations Guide\Volume 1 - Batch Overviews and Designs\
File Name: rms-120-og1

1. Oracle® Retail Merchandising System ORMS: Operations Guide (Release 12.0) (Electronic Data Interchange  Purchase Order Download).


Information Architecture Context diagram


Mapping spreadsheet

Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc156118519 \h 3
1.1	Purpose of Document	 PAGEREF _Toc156118520 \h 3
1.2	Background	 PAGEREF _Toc156118521 \h 3
1.3	Scope	 PAGEREF _Toc156118522 \h 3
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc156118523 \h 3
2.1	Description of the End-to-End Interface	 PAGEREF _Toc156118524 \h 3
2.2	Architecture	 PAGEREF _Toc156118525 \h 3
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc156118526 \h 3
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc156118527 \h 3
3.1	Scope	 PAGEREF _Toc156118528 \h 3
3.2	Source Message Schema	 PAGEREF _Toc156118529 \h 3
3.3	Message Transport Details	 PAGEREF _Toc156118530 \h 3
3.4	Naming and Configuration	 PAGEREF _Toc156118531 \h 3
3.5	Environment and Security Context	 PAGEREF _Toc156118532 \h 3
3.6	Non-Functional Requirements	 PAGEREF _Toc156118533 \h 3
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc156118534 \h 3
4.1	Scope	 PAGEREF _Toc156118535 \h 3
4.2	Data Validation	 PAGEREF _Toc156118536 \h 3
4.3	Filtering	 PAGEREF _Toc156118537 \h 3
4.4	Mapping	 PAGEREF _Toc156118538 \h 3
4.5	Target Message Schema	 PAGEREF _Toc156118539 \h 3
4.6	Sample Target Message	 PAGEREF _Toc156118540 \h 3
4.7	Message Transport Details	 PAGEREF _Toc156118541 \h 3
4.8	Naming and Configuration	 PAGEREF _Toc156118542 \h 3
4.9	Environment and Security Context	 PAGEREF _Toc156118543 \h 3
4.10	Non-Functional Requirements	 PAGEREF _Toc156118544 \h 3
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc156118545 \h 3
5.1	Scope	 PAGEREF _Toc156118546 \h 3
5.2	Data Validation	 PAGEREF _Toc156118547 \h 3
5.3	Filtering	 PAGEREF _Toc156118548 \h 3
5.4	Mapping	 PAGEREF _Toc156118549 \h 3
5.5	Target Message Schema	 PAGEREF _Toc156118550 \h 3
5.6	Message Transport Details	 PAGEREF _Toc156118551 \h 3
5.7	Naming and Configuration	 PAGEREF _Toc156118552 \h 3
5.8	Environment and Security Context	 PAGEREF _Toc156118553 \h 3
5.9	Non-Functional Requirements	 PAGEREF _Toc156118554 \h 3
6	Testing Deliverables	 PAGEREF _Toc156118555 \h 3
7	Deployment	 PAGEREF _Toc156118556 \h 3
8	Assumptions and Outstanding Issues	 PAGEREF _Toc156118557 \h 3
8.1	Assumptions	 PAGEREF _Toc156118558 \h 3
8.2	Outstanding Issues	 PAGEREF _Toc156118559 \h 3
Appendix A Volumes	 PAGEREF _Toc156118560 \h 3
Appendix B Glossary	 PAGEREF _Toc156118561 \h 3
Appendix C Document Control	 PAGEREF _Toc156118562 \h 3

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t the Purchase Order data between Retek Merchandising System (RMS) and Tesco Internet Management System (TIMS).

The document is of a sufficiently technical nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This document is for US and Turkey implementations. Two mapping documents will be prepared. Two different source codes will be written.

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including RMS and TIMS. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Purchase Order data from RMS into TIMS.
	
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
The interface is an extract of Purchase Order data from RMS by EDI batch process and transfer to a shared location via RTI File Adapter, and uploads into the TIMS system via integration layer BizTalk interfaces. The process is a full upload in nature.

The BizTalk interface is meant triggered by BizTalk orchestration to run at every 5 minutes time interval, which on completion is expected to produce a pipe | delimited flat-file (containing Purchase Order data records in required from by TIMS) FTP onto the shared location. This shared location would be monitored by TIMS system at the same interval. Once the file containing the extracted data appears on the shared location TIMS system will start the processing the Purchase Order data. The RMS Source message schema is not satisfying the needs of TIMS target message completely. The transformation process will pull the necessary data from IDS (Integrated Data Store) and merge with the RMS source data and generate the TIMS output file.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. Developers should put a ‘placeholder’ in their code / configurations as appropriate. 

Architecture
 EMBED Visio.Drawing.11  

Requirements for the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
To be finalised – requires discussion with RMS/TIMS team.
Performance Requirements
The scheduled batch job should be completed before the next batch of job gets scheduled.
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements

Operational Support Requirements
No such requirement has been agreed upon at the time of writing this document. However, it is perceived that there would be interface support requirements after go-live date that would require an evaluation.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
No such requirement till the time of writing this document.
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing required in an Extract-Stage of the interface
Scope
RMS pushes a positional flat file containing the Purchase Order data, to a predefined shared location. The flat file is created at a predefined time interval. Once the Purchase Order file created then an indicator file will be created for next catch and drop process. RTI File Adapter will transport the data file to shared location (Windows server) where BizTalk will look for the file. BizTalk will pickup the Purchase Order data file from the shared location. BizTalk will pool for the file every 5 minutes and picks up the file if available, transforms the file into a pipe | delimited flat file as specified in the target message schema and delivers the file to a shared location for TIMS for further processing. 
Source Message Schema
In this context, the source carries 2 different source data in the formats specified below. First Format is for US implementation. The second format is for Turkey implementation. The data files are positional files but variable record in length. Each row in the data file will carry first 5 characters as definition of row. Following table carries description column, which explain at row level and column level details.

Source Message Schema for RMS 10 of Turkey
Record NameField NameField TypeDefault ValueOccursDescriptionFHEAD



1:1


Record descriptor
Char(5)
FHEAD

File head marker

Line id
Char(10)
0000000001

Unique line id

Translator id
Char(5)
DLORD

Identifies transaction type

File create date
Char(14)


Current date YYYYMMDDHH24MISS format
Begin Group A1:*Mandatory and group can repeat multiple timesTORDR
Record descriptor
Char(5)
TORDR
1:1
Order header info

Line id
Char(10)


Unique file line id

Transaction id
Char(10)


Unique transaction id

Order change type
Char(2)


‘CH’ (changed) or ‘NW’ (new)

Order number
Number(8)


Internal Retek order no

Supplier
Number(10)


Internal Retek supplier id

Vendor order id
Char(15)
 

External vendor_order_no (if available)

Old order written date
Char(14)


Old date order created YYYYMMDDHH24MISS

New order written date
Char(14)


Changed date order created YYYYMMDDHH24MISS

Old Currency Code
Char(3)


Old order currency_code (ISO standard)

New Currency Code
Char(3)


Changed order currency_code (ISO standard)

Old Shipment Method of payment
Char(2)


Old ship_pay_method

New Shipment Method of Payment
Char(2)


Changed ship_pay_method

Old Transportation Responsibility
Char(2)


Old fob_trans_res

New Transportation Responsibility
Char(2)


Changed fob_trans_res

Old Trans.Resp. Description
Char(45)


Old fob_trans_res_desc

New Trans. Resp. Description
Char(45)


New fob_trans_res_desc

Old Title Passage Location
Char(2)


Old fob_title_pass

New Title Passage Location
Char(2)


Changed fob_title_pass

Old Title Passage Description
Char(45)


Old fob_title_pass_desc

New Title Passage Description
Char(45)


Changed fob_title_pass_desc

Old not before date
Char(14)


Old not_before_date YYYYMMDDHH24MISS

New not before date
Char(14)


Changed not_before_date YYYYMMDDHH24MISS

Old not after date
Char(14)


Old not_after_date YYYYMMDDHH24MISS

New not after date
Char(14)


Changed not_after_date YYYYMMDDHH24MISS

Old Purchase type
Char(6)


Old Purchase type

New Purchase type
Char(6)


New Purchase type

Backhaul allowance
Number(20)


Backhaul allowance

Old terms description
Char(240)


Old terms description from terms table

New terms description
Char(240)


New terms description from terms table

Old pickup date
Char(14)


Old pickup date YYYYMMDDHH24MISS

New pickup date
Char(14)


New pickup date YYYYMMDDHH24MISS

Old ship method
Char(6)


Old ship method

New ship method
Char(6)


New ship method

Old comment description
Char(250)


Old comment description

New comment description
Char(250)


New comment description

Supplier DUNS number
Number(9)


Supplier DUNS number

Supplier DUNS location
Number(4)


Supplier DUNS location
Begin Sub-Group AA1:*Mandatory and subgroup can repeat multiple times within Group ATITEM
File record descriptor
Char(5)

1:1
Item info

Line id
Char(10)


Unique line id

Transaction id
Char(10)


Unique transaction id

Item Number Type
Char(6)


Item_number_type

Item
Char(25)


Item (If a pack item this will be the pack number)

Old Ref Item Number type
Char(6)


Item_number_type for old ref_item

Old Ref Item
Char(25)


Old Ref_Item

New Ref Item Number type
Char(6)


Item_number_type for new ref_item

New Ref Item
Char(25)


Changed Ref_Item

Vendor catalog number
Char(30)


Supplier_item (VPN)

Free Form Description
Char(100)


item_desc

Supplier Diff 1
Char(80)


Supplier’s diff 1

Supplier Diff 2
Char(80)


Supplier’s diff 2

Item Parent
Char(25)


Required when Pack Template is not NULL

Pack template
Char(8)


Pack template associated w/style (packitem_breakout.pack_tmpl_id)

Template description
Char(40)


Description of pack template (if present) sups_pack_tmpl_desc.supp_pack_desc
TPACK



0 or *:1
Optional field. 0 or many TPACK record for one TITEM 

File record descriptor
Char(5)
TPACK

Pack component info

Line id
Char(10)


Unique line id

Transaction id
Char(10)


Unique transaction id

Pack id
Char(25)


Packitem_breakout.pack_no (same as item for the pack item)

Inner pack id
 Char(25)


Inner pack identification

Pack Quantity
Number(12)


Packitem_breakout.pack_item_qty (4 implied decimal places)

Component Pack Quantity
Number(12)


Packitem_breakout.comp_pack_qty (4 implied decimal places)

Item Parent Part Quantity
Number(12)


Packitem_breakout.item_parent_pt_qty (4 implied decimal places)

Item Quantity
Number(12)


Packitem_breakout.item_qty (4 implied decimal places)

Item Number Type
Char(6)


Item number type

Item
Char(25)


Item

Ref Item Number Type
Char(6)


Ref_item_number_type

Ref Item
Char(25)


Ref_item

VPN
Char(30)


Supplier item (vpn)

Supplier Diff 1
Char(80)


Supplier’s diff 1

Supplier Diff 2
Char(80)


Supplier’s diff 2

Item Parent
Char(25)


Required when Pack Template is not NULL

Pack template
Char(8)


Pack template associated w/style (packitem_breakout.pack_tmpl_id)

Template description
Char(40)


Description of pack template (if present) sups_pack_tmpl_desc.supp_pack_desc
Begin Sub Sub-Group AAA1:*Mandatory and subgroup can repeat multiple times within sub-Group AATSHIP



1:1
Mandatory field. One or many Shipping detail should be for one TITEM

Record type
Char(5)
TSHIP

Describes file record-shipment info

Line id
Char(10)


Unique file line number

Transaction id
Char(10)


Unique transaction number

Location type
Char(2)


‘ST’ store or ‘WH’ warehouse

Ship to location
Number(10)


Location value form ordloc (store or wh)

Old unit cost
Number(20)


Old unit cost (4 implied decimal places)

New unit cost
Number(20)


New unit cost (4 implied decimal places)

Old quantity
Number(12)


Old qty_ordered or qty_allocated (4 implied decimal places)

New quantity
Number(12)


Changed qty_ordered or qty_allocated (4 implied decimal places)

Old outstanding quantity
Number(12)


Old qty_ordered-qty_received (4 implied decimal places)(or qty_allocated-qty transferred for an allocation)

New outstanding quantity
Number(12)


Changed qty_ordered-qty_received (4 implied decimal places)(or qty_allocatedqty_transferred for an allocation)

Cancel code
Char(1)




Old cancelled quantity
Number(12)


Previous quantity cancelled (4 implied decimal places)

New cancelled quantity
Number(12)


Changed quantity cancelled (4 implied decimal places)

Quantity type flag
Char(1)


‘S’hip to ‘A’llocate

 Store or warehouse indicator
Char(2)


‘ST’ (store) or ‘WH’ (warehouse)

Old x-dock location
Number(10)


Alloc_detail location (store or wh)

New x-dock location
Number(10)


Alloc_detail location (store or wh)

Case length
Number(12)


Case length (4 implied decimal places)

Case width
Number(12)


Case width (4 implied decimal places)

Case height
Number(12)


Case height (4 implied decimal places)

Case LWH unit of measure
Char(4)


Case LWH unit of measure

Case weight
Number(12)


Case weight (4 implied decimal places)

Case weight unit of measure
Char(4)


Case weight unit of measure

Case liquid volume
Number(12)


Case liquid volume (4 implied decimal places)

Case liquid volume unit of measure
Char(4)


Case liquid volume unit of measure

Location DUNS number
Number(9)


Location DUNS number

Location DUNS loc
Number(4)


Location DUNS loc

New unit cost init
Number(20)


New unit cost init (4 implied decimal places)

Old unit cost init
Number(20)


Old unit cost init (4 implied decimal places)

Item/loc discounts
Number(20)


Item/loc discounts (4 implied decimal places)
End Sub Sub-Group AAAEnd Sub-Group AATTAIL



1:1
Mandatory and occurs only once in Group A

Record type
Char(5)
TTAIL

Describes file record – marks end of order

Line id
Char(10)


Unique file line id

Transaction id
Char(10)


Unique transaction id

#lines in transaction
Number(10)


#lines in transaction
End
Group AFTAIL



1:1
Mandatory and occurs only once in the entire file

Record type
Char(5)
FTAIL

Describes file record – marks end of file

Line id
Char(10)


Unique file line id

#lines
Number(10)


Total number of transaction lines in file (not including FHEAD and FTAIL)
	

Source Schema is from Retek Merchandizing System 12T for US
Record
Name
Field NameField TypeDefault  ValueOccursDescriptionFHEAD



1:1
Mandatory and occurs only once in the entire file

Record descriptor
Char(5)
FHEAD

File head marker

Line id
Number(10)
0000000001

Unique line id

Translator id
Char(5)
DLORD

Identifies transaction type

File create date

Char(14)



Vdate in YYYYMMDDHH24MISS
Format
Begin Group A1:*Mandatory and group can repeat multiple timesTORDR
Record descriptor
Char(5)
TORDR
1:1
Order header information

Line id
Number(10)


Unique file line id

Transaction id
Number(10)


Unique transaction id

Order change type
Char(2)


‘CH’ (changed) or ‘NW’(new)

Order number
Number(8)


Internal Oracle Retail order no

Supplier
Number(10)


Internal Oracle Retail supplier id

Vendor order id

Char(15)



External vendor_order_no (if
available)

Order written date

Char(14)



Order created date in
YYYYMMDDHH24MISS
Format

Original order approval date

Char(14)



Original order approval date
in YYYYMMDDHH24MISS
Format

Old Currency Code
Char(3)



Old order currency_code
(ISO standard)

New Currency Code
Char(3)



Changed order currency_code (ISO standard)

Old Shipment Method of Payment
Char(2)



Old ship_pay_method

New Shipment Method of Payment
Char(2)



Changed ship_pay_method

Old Transportation
Responsibility
Char(2)



Old fob_trans_res


Old Transportation
Responsibility
Description
Char(250)



Old fob_trans_res_desc


New Transportation
Responsibility
Char(2)



Changed fob_trans_res

New Trans. Resp.
Description
Char(250)



New fob_trans_res_desc


Old Title Passage
Location
Char(2)



Old fob_title_pass


New Title Passage
Location
Char(2)



Changed fob_title_pass


Old Title Passage
Description
Char(250)



Old fob_title_pass_desc


New Title Passage
Description
Char(250)



Changed fob_title_pass_desc


Old not before date

Char(14)



Old not_before_date in
YYYYMMDDHH24MISS
Format

New not before
Date
Char(14)



Changed not_before_date in
YYYYMMDDHH24MISS
Format

Old not after date
Char(14)


Old not_after_date in
YYYYMMDDHH24MISS
Format

New not after date
Char(14)



Changed not_after_date in
YYYYMMDDHH24MISS
Format

Old Purchase type
Char(6)


Old Purchase type

New Purchase Type
Char(6)


New Purchase type

Backhaul Allowance
Char(20)


Backhaul allowance

Old terms Description
Char(240)



Old terms description from
terms table

New terms Description
Char(240)



New terms description from
terms table

Old pickup date

Char(14)



Old pickup date
YYYYMMDDHH24MISS

New pickup date
Char(14)


New pickup date
YYYYMMDDHH24MISS

Old ship method
Char(6)


Old ship method

New ship method
Char(6)


New ship method

Old comment Description
Char(2000)


Old comment description

New comment Description
Char(2000)



New comment description


Supplier DUNS Number
Char(9)



Supplier DUNS number


Supplier DUNS Location
Char(4)



Supplier DUNS location

Begin Sub-Group AA1:*Mandatory and subgroup can repeat multiple times within Group ATITEM

File record descriptor
Char(5)
TITEM
1:1
Item info

Line id
Number(10)


Unique line id

Transaction id
Number(10)


Unique transaction id

Item Number Type
Char(6)


Item_number_type

Item
Char(25)



Item (For a pack item, this is
the pack number)

Old Ref Item Number type
Char(6)



Item_number_type for old
ref_item

Old Ref Item
Char(25)


Old Ref_Item

New Ref Item
Number type
Char(6)


Item_number_type for new
ref_item

New Ref Item
Char(25)


Changed Ref_Item

Vendor catalog
Number
Char(30)


Supplier_item (VPN)


Free Form
Description
Char(250)



Item_desc


Supplier Diff 1
Char(120)


Supplier’s diff 1

Supplier Diff 2
Char(120)


Supplier’s diff 2

Supplier Diff 3
Char(120)


Supplier’s diff 3

Supplier Diff 4
Char(120)


Supplier’s diff 4

Pack Size

Number(12)



Supplier defined pack size *
10000 (4 implied decimal
places)
TPACK



0:1
Optional field. 0 or many TPACK record for one TITEM 

File record
descriptor
Char(5)

TPACK


Pack component info


Line id
Number(10)


Unique line id

Transaction id
Number(10)


Unique transaction id

Pack id

Char(25)



Packitem_breakout.pack_no
(same as item for the pack
item)

Inner pack id
Char(25)


Inner pack identification

Pack Quantity

Number(12)



Packitem_breakout.pack_item_
qty*10000 (4 implied decimal places)

Component Pack
Quantity

Number(12)



Packitem_breakout.comp_pack_
qty*10000 (4 implied decimal places)

Item Parent Part
Quantity

Number(12)



Packitem_breakout.item_pare
nt_pt_qty*10000 (4 implied
decimal places)

Item Quantity

Number(12)



Packitem_breakout.item_qty*
10000 (4 implied decimal
places)

Item Number
Type
Char(6)



Item number type


Item
Char(25)


Item

Ref Item Number
Type
Char(6)


Ref_item_number_type

Ref Item
Char(25)


Ref_item

VPN
Char(30)


Supplier item (vpn)

Supplier Diff 1
Char(120)


Supplier’s diff 1

Supplier Diff 2
Char(120)


Supplier’s diff 2

Supplier Diff 3
Char(120)


Supplier’s diff 3

Supplier Diff 4
Char(120)


Supplier’s diff 4

Item Parent

Char(25)



Required when Pack
Template is not NULL

Pack template

Number(8)



Pack template associated
w/style
(packitem_breakout.pack_tm
pl_id)

Template
description

Char(250)



Description of pack template.
sups_pack_tmpl_desc.supp_p
ack_desc
Begin Sub Sub-Group AAA1:*TSHIP



1:1
Mandatory field. One or many Shipping detail should be for one TITEM

Record type

Char(5)

TSHIP


Describes the file recordshipment
Information

Line id
Number(10)


Unique file line number

Transaction id
Number(10)


Unique transaction number

Location type

Char(2)



‘ST’ store or ‘WH’ warehouse

Ship to location

Number(10)



Location value form ordloc
(store or warehouse)

Old unit cost

Number(20)



Old unit cost*10000 (4 implied decimal places)

New unit cost

Number(20)



New unit cost*10000 (4 implied decimal places)

Old quantity

Number(12)



Old qty_ordered *10000 or
qty_allocated*10000 (4 implied decimal places)

New quantity

Number(12)



Changed qty_ordered*10000
or qty_allocated*10000 (4 implied decimal places)

Old outstanding
quantity

Number(12)



Old (qty_ordered-qty_
received)*10000 or
(qty_allocated-qty
transferred)*10000 for an
allocation
(4 implied decimal places)

New outstanding
quantity

Number(12)



Changed qty_ordered-qty_
received (4 implied decimal places)(or qty_allocated-qty_
transferred, for an allocation)

Cancel code
Char(1)




Old cancelled
Quantity
Number(12)



Previous quantity cancelled
(4 implied decimal places)

New cancelled
Quantity
Number(12)



Changed quantity cancelled
(4 implied decimal places)

Quantity type flag
Char(1)


‘S’hip to ‘A’llocate

Store or warehouse
indicator
Char(2)



‘ST’ (store) or ‘WH’
(warehouse)

Old x-dock
Location
Number(10)



Alloc_detail location (store or wh)

New x-dock
Location
Number(10)



Alloc_detail location (store or wh)


Case length
Number(12)



Case length (4 implied decimal places)

Case width

Number(12)



Case width (4 implied decimal places)

Case height

Number(12)



Case height (4 implied decimal places)

Case LWH unit of
measure
Char(4)



Case LWH unit of measure


Case weight

Number(12)



Case weight (4 implied
decimal places)

Case weight unit of measure
Char(4)



Case weight unit of measure


Case liquid volume
Number(12)



Case liquid volume (4 implied decimal places)

Case liquid volume unit of measure
Char(4)



Case liquid volume unit of
Measure

Location DUNS number
Char(9)


Location DUNS number

Location DUNS loc
Char(4)


Location DUNS loc

Old unit cost init

Number(20)



Old unit cost init (4 implied
decimal places)

New unit cost init

Number(20)



New unit cost init (4 implied
decimal places)

Item/loc discounts

Number(20)



Item/loc discounts (4 implied
decimal places)
End Sub Sub-Group AAAEnd Sub-Group AATTAIL

Record type

Char(5)

TTAIL

1:1
Describes file record – marks
end of order

Line id
Number(10)


Unique file line id

Transaction id
Number(10)


Unique transaction id

#Lines in
Transaction
Number(10)



Number of lines in
Transaction
End
Group AFTAIL

Record type

Char(5)

FTAIL

1:1
Describes file record – marks
end of file

Line id
Number(10)


Unique file line id

#lines

Number(10)



Total number of transaction
lines in file (not including
FHEAD and FTAIL)

Sample Source Message
FHEAD0000000001TSCPODNLD_v1.5      20060503014430S0000009002
TORDR00000000020000000001NW565016  0000341967               2006050200000020060502000000TRYTRY                                                                                                  OVOVFOB POINT                                    FOB POINT                                    20060512000000200605120000002006051200000020060512000000            000000000000000000005 Gün                                                                                                                                                                                                                                           5 Gün                                                                                                                                                                                                                                           2006051200000020060512000000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
TITEM00000000030000000001ITEM  100027294                                               EAN13 4007383192908                                          BÜYÜKLER ÝÇÝN DALIÞ MASKESÝ                                                                                                                                                                                                                                                                                                                                                                                                         000000010000
TSHIP00000000040000000001ST00000090020000000000000000000000000000000000026900000000000000000011880000000000000000000011880000 000000000000000000000000S                      000000000000000000000000000000000000    000000000000    000000000000                 000000000000000000000000000000000002690000000000000000000000
TITEM00000000050000000001ITEM  100680015                                               EAN13 4007383118304                                          ÞÝÞME TAMÝR SETÝ                                                                                                                                                                                                                                                                                                                                                                                                                    000000010000
TSHIP00000000060000000001ST00000090020000000000000000000000000000000000016500000000000000000005040000000000000000000005040000 000000000000000000000000S                      000000000000000000000000000000000000    000000000000    000000000000                 000000000000000000000000000000000001650000000000000000000000
TTAIL000000000700000000010000000006
TORDR00000000080000000002NW565113  0000189447               2006050200000020060502000000TRYTRY                                                                                                  OVOVFOB POINT                                    FOB POINT                                    20060601000000200606010000002006060100000020060601000000            0000000000000000000095 Gün                                                                                                                                                                                                                                          95 Gün                                                                                                                                                                                                                                          2006060100000020060601000000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
TITEM00000000090000000002ITEM  101153946                                               EAN13 8711295599521            XX3500000                     ÝTHAL AHÞAP KLASÝK SALLANAN SANDALYE                                                                                                                                                                                                                                                                                                                                                                                                000000010000
TSHIP00000000100000000002ST00000090020000000000000000000000000000000000821300000000000000000000640000000000000000000000640000 000000000000000000000000S                      000000000000000000000000000000000000    000000000000    000000000000                 000000000000000000000000000000000082130000000000000000000000
TTAIL000000001100000000020000000004
TORDR00000000120000000003NW566456  0000341967               2006050200000020060502000000TRYTRY                                                                                                  OVOVFOB POINT                                    FOB POINT                                    20060512000000200605120000002006051200000020060512000000            000000000000000000005 Gün                                                                                                                                                                                                                                           5 Gün                                                                                                                                                                                                                                           2006051200000020060512000000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
TITEM00000000130000000003ITEM  100027294                                               EAN13 4007383192908                                          BÜYÜKLER ÝÇÝN DALIÞ MASKESÝ                                                                                                                                                                                                                                                                                                                                                                                                         000000010000
TSHIP00000000140000000003ST00000090020000000000000000000000000000000000026900000000000000000011880000000000000000000011880000 000000000000000000000000S                      000000000000000000000000000000000000    000000000000    000000000000                 000000000000000000000000000000000002690000000000000000000000
TITEM00000000150000000003ITEM  100680015                                               EAN13 4007383118304                                          ÞÝÞME TAMÝR SETÝ                                                                                                                                                                                                                                                                                                                                                                                                                    000000010000
TSHIP00000000160000000003ST00000090020000000000000000000000000000000000016500000000000000000005040000000000000000000005040000 000000000000000000000000S                      000000000000000000000000000000000000    000000000000    000000000000                 000000000000000000000000000000000001650000000000000000000000
TTAIL000000001700000000030000000006
FTAIL00000000180000000016


Message Transport Details
Feature
Specification
Additional Information
Source System Name
RMS

Source Platform / OS
IBM AIX

Source Physical Location


Source Underlying Data Storage Technology


Target System Name
Biztalk 2006

Target Platform / OS
Biztalk 2006 Server

Target Physical Location


Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
RTI File Adaptor		
                 (XCOM) 	

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
N/A

Logging
Log via the Operational Framework.

Error Handling
On fail move the file to the failed transmissions location.



Naming and Configuration

BizTalk
Package Name: Tesco_TOM_Purchase_Order_For_TIMS
BizTalk Procedure
Name
USP_Tesco_TOM_Purchase_Order
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Environment and Security Context
 
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements

No Such requirement till time of writing this document.

Processing required in the Messaging Stage of the interface
Scope
BizTalk orchestration monitors the Purchase order file arrival, which is created via EDI batch in the shared location (Windows server) for every new data file and submits the same for transformation and upload.
Data Validation
Data type and Length Validation will be done by BizTalk the integrity check will be done by target TIMS system.
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.

Please refer the spreadsheet at <location>
Target Message Schema
Code
Optional
Type
Description
PO Header:
RECTYPE

CHAR(1)
Type of record “H”
ACTION

CHAR(1)
PO status 
“N” – new
“C” – changed
ECONMAG

NUMBER(10)
site ID (Tesco Shop ID)
ECONCOM

NUMBER(8)
purchase order ID
ECOCNUF

NUMBER(9)
supplier ID
ECODCOM

CHAR(8)
purchase order date
ECODLIV

CHAR(8)
scheduled delivery date
ECODMAJ
Yes
CHAR(8)
time updated
ECOUTIL

CHAR(6)
user name
ADRRAIS

CHAR(35)
Supplier - corporate name
ADRRUE1

CHAR(35)
Supplier - street ( 1 )
ADRRUE2

CHAR(35)
Supplier - street ( 2 )
ADRVILL

CHAR(35)
Supplier – city
ADRCODE

CHAR(9)
Supplier – zipcode
ADRTELC
Yes
CHAR(16)
Supplier – fax nr
ADRTELP
Yes
CHAR(16)
Supplier - telephone nr
PARLIBL

CHAR(20)
long description – country
MADRAIS_COMM

CHAR(35)
Site raising order - corporate name
MADRUE1_COMM

CHAR(35)
Site raising order – street ( 1 )
MADRUE2_COMM

CHAR(35)
Site raising order – street ( 2 )
MADVILL_COMM

CHAR(35)
Site raising order – city
MADCODE_COMM

CHAR(9)
Site raising order – zipcode
MADTELP_COMM
Yes
CHAR(16)
Site raising order - telephone nr
MADTELC_COMM
Yes
CHAR(16)
Site raising order - fax nr
PARLIBL_COMM

CHAR(20)
Site raising order – country
MADRAIS_FACT

CHAR(35)
Invoice address - corporate name
MADRUE1_FACT

CHAR(35)
Invoice address - street ( 1 )
MADRUE2_FACT

CHAR(35)
Invoice address - street ( 2 )
MADVILL_FACT

CHAR(35)
Invoice address – city
MADCODE_FACT

CHAR(9)
Invoice address – zipcode
MADTELP_FACT

CHAR(16)
Invoice address - telephone nr
MADTELC_FACT
Yes
CHAR(16)
Invoice address - fax nr
PARLIBL_FACT
Yes
CHAR(20)
Invoice address – country
MADRAIS_LIVR

CHAR(35)
Delivery address - corporate name
MADRUE1_LIVR

CHAR(35)
Delivery address – street ( 1 )
MADRUE2_LIVR

CHAR(35)
Delivery address – street ( 2 )
MADVILL_LIVR

CHAR(35)
Delivery address – city
MADCODE_LIVR

CHAR(9)
Delivery address - zipcode
MADTELP_LIVR

CHAR(16)
Delivery address - telephone nr
MADTELC_LIVR
Yes
CHAR(16)
Delivery address - fax nr
PARLIBL_LIVR
Yes
CHAR(20)
Delivery address - country
DCOCOLI
Yes
NUMBER(6)
quantity in cartons
DCOQTEP
Yes
NUMBER(6)
quantity in pallets
DCOQTEC
Yes
NUMBER(11,3)
quantity ( selling unit )
WEIGHT
Yes
NUMBER(11,3)
Weight
ECOLIGN
Yes
CHAR(60)
Comment
ECOLIG2
Yes
CHAR(60)
Comment
ECODEVI

VARCHAR2(3)
Currency 
ECOGLN
Yes
NUMBER (13)
GLN ship from (NULL value means default GLN from TIMS will be used)
PO Items:
RECTYPE

CHAR(1)
Type of record “L”
DCOEAN13

CHAR(14)
TPN
DCOPVSA

NUMBER(11,3)
net purchase price
ARTLIBL

CHAR(30)
article - long description
DCOSPCB
Yes
NUMBER(4)
SKU per sub-carton
DCOPCB

NUMBER(4)
SKU per carton
PCBPAL

NUMBER(4)
Cartons per pallet
ARTPBRU

NUMBER(8,3)
Gross weight
DCOQTEC

NUMBER(9,3)
quantity ( selling unit )
ARCRCOM
Yes
CHAR(13)
reorder code, SPN (VPN)
EAN_ID

CHAR(13)
Cash register article code, EAN/UPC/GS1 Barcode, OCC
DCOCOLI

NUMBER(9,3)
quantity in purchase unit
DCOQTEP

NUMBER(9,3)
ordered quantity (pallets)
DCOPUT

CHAR(10)
Purchase unit name
DCOUAUVC

NUMBER (9,3)
Number of SKU in Purchase unit (=DCOQTEC / DCOCOLI)
DCOPRIX

NUMBER(11,3)
Purchase price 
DCOIORD

NUMBER(6)
Original PO line item number
PO Store Distribution
RECTYPE

CHAR(1)
Type of record “S”
EDCDSITE

NUMBER(10)
destination site
EDCSITLIB

CHAR(35)
name of site
EDCDUAUVC

NUMBER(9,3)
Number of SKU/purchase unit
EDCDQTEC

NUMBER(9,3)
SKU quantity for the site
EDCDQTUA

NUMBER(9,3)
PU quantity for the site
EDCDNREQ
Yes
NUMBER(8)
destination site order number 
EDCDDCRE
Yes
CHAR(8)
creation date of site order

Sample Target Message
The source message is from RMS and in the form of positional flat file and is getting converted to the target file format (pipe | delimited flat file) in a package. The following message format is the target message format. 

Message Transport Details 
For messages destined for TIMS system, the following applies.	

Feature
Specification
Additional Information
Source System Name
Biztalk 2006

Source Platform / OS
Biztalk 2006 Server

Source Physical Location


Source Underlying Data Storage Technology
File System

Target System Name
TIMS

Target Platform / OS
LINUX

Target Physical Location


Target Underlying Data Storage Technology


Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		

Data Format

XML  				
Delimited 			
Positional 			

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
Not yet decided

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.


Naming and Configuration

Biztalk
Instruction Name: Tesco_TOM_Purchase_Order_for_TIMS_File_Delivery
Instruction Details
Description
To be determined
Enabled
Activate
Type

Operational Window
Schedule
N/A
Enabled
False
Port Details
Receive Port

Receive Location

Receive Pipeline

Transport

Message Type

Receive Folder

Batch

No. of Messages

Max. Batch Size

Operational Details
Worker Threads

Priority

Period

Retry Attempts

Timeout

Require Data Send

Exception Management

Treat Fatal Adapter Exception As

Treat Unhandled Exceptions As




Environment and Security Context
Messaging will happen through BizTalk. The BizTalk2006 EAI tool will be set with the Environment specification (will be defined)

Account details will be included here once we have visibility of the environments.

Non-Functional Requirements
On successful delivery of the file to the target system, the audit log should be updated via the Operational Framework pipeline component or adapter (to be determined).

In the event of a failure the file should be written to the failed files location, and an alert should be raised.


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

Naming and Configuration
Not Required
Environment and Security Context
Not Required

Non-Functional Requirements
Testing Deliverables
Unit Test Scripts and test cases are kept at the following location <location>Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1
The input file from RMS is assumed to be less than 10MB in size. Technology expert says that Messaging more than 10 MB through BizTalk is not advisable.



Outstanding Issues
ID
Issue
To be addressed by
1
File naming format to be confirmed
Andrew Barker
2
Server Physical Location of the server and file 
Andrew Barker
3
Failure handling
Andrew Barker





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
Interface
Interface
Many definitions exist for 'interface'. In general, 'interface' refers to the link between a data source and a data target. And there are properties of the interface in this context. However more specifically 'interface' refers to one end of a data link, hence the terms source interface and target interface, and both the source interface and the target interface will have specific properties of their own.
RMS
Retek Merchandising System
Retek Merchandising System is getting installed for TESCO Merchandising operations in US. This system will governs the Merchandising operations; Receive base Master & Transaction data and from other systems and Provide data to next level of operation system as part of Retail systems chain.
TIMS
TESCO Internet Management System
TESCO Internet Management System is a gateway for the TESCO suppliers to access the data and give their responses. For TIMS the main data feed will be from RMS.
FHEAD
File Header Record
This is File header record identifier. This string will get inserted at the beginning of the file. 
TORDR
Purchase Order Header Record
This is new Purchase Order Record identifier. This string will get inserted at the beginning of every new PO details.
TITEM
Item Detail Record
This is Item record identifier within a Purchase Order. This string will get inserted for Item Number within a PO.
TPACK
Pack etail Record
This is Item Pack record identifier. This string will get inserted at the beginning of every Pack Item. This is linked to TITEM record. 
TSHIP
Shipment Detail Record
This is Shipment record identifier. This string will get inserted at the beginning of every Shipment detail record against the Item. This is linked to TITEM record.
TTAIL
Purchase Order Tail Record
This is Purchase Order end of record identifier.  This string will get inserted at the beginning of every end of purchase order transaction. This record to identify end of purchase order transaction. 
FTAIL
File Tail Record
This is File tail record identifier. This stringed record will get inserted to identify the end of file.   
IDS
Integrated Data Store
Integrated Data Store (IDS) is a staging area for TOM project. In IDS, reference data will get stored in periodical bases. Any transformation process needed additional information to be referenced or passed to the target schema, will refer IDS.
	
Document Control
Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
27-Dec-2006
0.1D
Draft
Supriyo Chakraborty
28-Dec-2006
0.2D
Draft
Sankar G
03-Jan-2007
0.3D
Draft
Sankar G
09-Jan-2007
0.4D
Draft
Supriyo Chakraborty
17-Jan-2007
0.5D
Draft
Sankar G
30-Jan-2007
1.0 
First Release



Related Documents

Author	
Date
Version
Title
<to be Filled up>

















Distribution

Name
Position
Approver/Contributor/Other
Andrew Barker
Solution Architect

David Onyett
Project Lead

Nathan Smith
Enterprise Architect




















Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER Error! Reference source not found., Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 17 of  NUMPAGES 31	Date:  SAVEDATE \@ "d MMM yyyy" 30 Jan 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































