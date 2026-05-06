## Mapping
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 | Unnamed: 10 | Unnamed: 11 | Unnamed: 12 | Unnamed: 13 | Unnamed: 14 | Unnamed: 15 | Unnamed: 16 | Unnamed: 17 | Unnamed: 18 | Unnamed: 19 | Unnamed: 20 | Unnamed: 21 | Unnamed: 22 | Unnamed: 23 | Unnamed: 24 | Unnamed: 25 | Unnamed: 26 | Unnamed: 27 | Unnamed: 28 | Unnamed: 29 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | IDS Pack Item to GFO | NaN | NaN | NaN | NaN | Version 1.0.0 | NaN | NaN | NaN | NaN | NaN | NaN | Notes/Issues Key | NaN | NaN | NaN | NaN | NaN | NaN | Key to Mandatory Column | NaN | NaN | NaN | NaN | NaN | Assumption | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Business | NaN | NaN | NaN | NaN | NaN | Y | Required | NaN | NaN | NaN | NaN | 1 | For column Justified,the L means Left side of the viewer & R means Right side of the viewer | NaN | NaN |
| NaN | Source format: Database | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Technical | NaN | NaN | NaN | NaN | NaN | N | Optional | NaN | NaN | NaN | NaN | 2 | Table SKUItemLevel2 primary key field [SKUID] taken as Item No. | NaN | NaN |
| NaN | Source record structure - Database | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Business/Technical | NaN | NaN | NaN | NaN | NaN | C | Conditional - see notes/issues | NaN | NaN | NaN | NaN | 3 | Table StyleItemLevel1 field [STYLEID] is the foregion key of SKUItemLevel2 primary key field [SKUID] | NaN | NaN |
| NaN | Source interface: IDS Items-Region | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Maps | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 4 | Table StyleItemLevel1 field [Section],[Class],[SubClass] fields were foregion key of table Section,Class & SubClass | NaN | NaN |
| NaN | Target File Name: JLL.IL.JLBPO.PROD.CTRY | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Not mapped/Set Field Value | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 5 | Table Class has [Section] as the foregion key of table Section. | NaN | NaN |
| NaN | Target file format: Flat file | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set by Integration Layer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 6 | Table Section has [Department] as the foregion key of table Department. | NaN | NaN |
| NaN | Target Record Structure -  positional fields, record terminator LF(x0A) | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 7 | Table Department has [Divison] as the foregion key of table Divison. | NaN | NaN |
| NaN | Integration to use "Target" for mandatory and data validation rules. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | HEADER: Record type = 0\nDETAIL: Record type = 1\nTRAILER - Record type = 9 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Notes:This mapping is used to populate the ‘product’ and ‘product in region’ information into GFO from IDS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Transaction unit: NA | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source - IDS (Database: ??) | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Target - GFO | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | RECORD Type | Field No# | Table / Object Name | Field Name / Description | Data Type | Field Start Pos. | Field End Pos. | Field\nSize | Mandatory | Transformation / Condition | Format | Justified (L = Left, R = Right) | Pad Char. | NaN | RECORD Type | Field No# | Table / Object Name | Field Name / Description | Data Type | Field Start Pos. | Field End Pos. | Field Size | Mandatory | Transformation / Condition | Format | Justified (L = Left, R = Right) | Pad Char. | NaN | Notes/Issues |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Header | 1 | NaN | JLBOA-REC-TYPE | Char | 1 | 1 | 1 | Y | NaN | 0 | NaN | NaN | NaN | Integration layer to set the record type to 0 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Header | 2 | NaN | JLBOA-DATE | Char | 2 | 11 | 10 | Y | NaN | CCYYMMDD | NaN | NaN | NaN | Integration layer to set the value to system date in the format mentioned |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Header | 3 | NaN | FILLER | Char | 12 | 170 | 159 | N | NaN | X(159) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 1 | NaN | JLBOB-REC-TYPE | Char | 1 | 1 | 1 | Y | NaN | 1 | NaN | NaN | NaN | Integration layer to set the record type to 1 for detail |
| NaN | NaN | NaN | SKUItemLevel2 | SKUID | varchar(25) | NaN | NaN | NaN | NaN | Required to convert into Numeric type | NaN | NaN | NaN | NaN | Detail | 2 | NaN | JLBOB-BASE-PRODUCT-NO | Numeric | 2 | 10 | 9 | Y | NaN | 9(9) | L | NaN | NaN | Assuming Source data is numeric, length of Source data is <=9, and Source is LEFT JUSTIFIED |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 3 | NaN | JLBOB-BPR-REGN | Char | 11 | 12 | 2 | Y | NaN | X(2) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 4 | NaN | JLBOB-BASE-PROD-RNGE-CLASS | Char | 13 | 14 | 2 | Y | NaN | X(2) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 5 | NaN | JLBOB-BPR-METRO-RCLASS | Char | 15 | 16 | 2 | Y | NaN | X(2) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 6 | NaN | JLBOB-STORE-ORDERABLE-IND | Char | 17 | 17 | 1 | Y | NaN | X | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 7 | NaN | JLBOB-DEVELOPMENT-LINE | Char | 18 | 18 | 1 | Y | NaN | X | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 8 | NaN | JLBOB-DIAMOND-PROD-IND | Char | 19 | 19 | 1 | Y | NaN | X | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 9 | NaN | JLBOB-SRCE-TYPE-IND | Char | 20 | 20 | 1 | Y | NaN | X | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 10 | NaN | JLBOB-ORDER-GROUP | Char | 21 | 22 | 2 | Y | NaN | X(2) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 11 | NaN | JLBOB-RMS-COMM-HIER | Char | 23 | 42 | 20 | Y | NaN | X(20) | NaN | NaN | NaN | Cocatenated field known as SubGroup in GFO system |
| NaN | NaN | NaN | Divison | Divison | Smallint | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 12 | NaN | JLBOB-RMS-DIVISION | Numeric | 23 | 26 | 4 | Y | NaN | 9(4) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | Department | Department | Smallint | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 13 | NaN | JLBOB-RMS-GROUP | Numeric | 27 | 30 | 4 | Y | NaN | 9(4) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | Section | Section | Smallint | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 14 | NaN | JLBOB-RMS-DEPT | Numeric | 31 | 34 | 4 | Y | NaN | 9(4) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | Class | Class | Smallint | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 15 | NaN | JLBOB-RMS-CLASS | Numeric | 35 | 38 | 4 | Y | NaN | 9(4) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | SubClass | SubClass | Smallint | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 16 | NaN | JLBOB-RMS-SUBCLASS | Numeric | 39 | 42 | 4 | Y | NaN | 9(4) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | SKUItemLevel2 | ItemDesc | varchar(250) | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 17 | NaN | JLBOB-BASE-PROD-DESCRIPTION | Char | 43 | 90 | 48 | Y | NaN | X(48) | L | NaN | NaN | Only 48 characters extracted out of 290 character source length. Rest will be truncated on right |
| NaN | NaN | NaN | SKUItemLevel2 | StandardUOM | varchar(4) | NaN | NaN | NaN | NaN | If (Standard\_UOM== "EA") then "I" else "W" | NaN | NaN | NaN | NaN | Detail | 18 | NaN | JLBOB-SELL-WT-ITEM-IND | Char | 91 | 91 | 1 | Y | NaN | X | L | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 19 | NaN | JLBOB-SALEABLE-EFF-DATE | Char | 92 | 101 | 10 | Y | NaN | X(10) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | SKUItemLevel2 | StandardUOM | varchar(4) | NaN | NaN | NaN | NaN | if(SKUItemLevel2 ->> Standard\_UOM)== "EA" then "SNGL"\nelse \nSKUItemLevel2 ->> Standard\_UOM | NaN | NaN | NaN | NaN | Detail | 20 | NaN | JLBOB-S-B-W-UNIT-MEASURE | Char | 102 | 105 | 4 | Y | NaN | X(4) | NaN | NaN | NaN | Does this transformation logic need to be embedded in mapping or do we need to refer some lookup table |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 21 | NaN | JLBOB-UNIT-SIZE | Float | 106 | 112 | 7 | Y | NaN | 9(5)V99 | NaN | NaN | NaN | Set to spaces. This is still being evaluated and is subject to change |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 22 | NaN | JLBOB-LOW-LEVEL-GRP-CD | Char | 113 | 114 | 2 | Y | NaN | X(2) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 23 | NaN | JLBOB-BASE-PROD-SEQ-NO | Char | 115 | 117 | 3 | Y | NaN | X(3) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 24 | NaN | JLBOB-DGRP-CODE | Char | 118 | 120 | 3 | Y | NaN | X(3) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 25 | NaN | JLBOB-MERCH-GRP-CODE | Char | 121 | 123 | 3 | Y | NaN | X(3) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 26 | NaN | JLBOB-SUPP-MERCHG-GRP-CODE | Char | 124 | 126 | 3 | Y | NaN | X(3) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 27 | NaN | JLBOB-MIN-SHELF-LIFE | Numeric | 127 | 129 | 3 | Y | NaN | 9(3) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 28 | NaN | JLBOB-EXPCTD-SHELF-LIFE-1 | Numeric | 130 | 132 | 3 | Y | NaN | 9(3) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 29 | NaN | JLBOB-DELY-AVAILABLE-IND-1 | Char | 133 | 133 | 1 | Y | NaN | X | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 30 | NaN | JLBOB-EXPCTD-SHELF-LIFE-2 | Numeric | 134 | 136 | 3 | Y | NaN | 9(3) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 31 | NaN | JLBOB-DELY-AVAILABLE-IND-2 | Char | 137 | 137 | 1 | Y | NaN | X | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 32 | NaN | JLBOB-EXPCTD-SHELF-LIFE-3 | Numeric | 138 | 140 | 3 | Y | NaN | 9(3) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 33 | NaN | JLBOB-DELY-AVAILABLE-IND-3 | Char | 141 | 141 | 1 | Y | NaN | X | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 34 | NaN | JLBOB-EXPCTD-SHELF-LIFE-4 | Numeric | 142 | 144 | 3 | Y | NaN | 9(3) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 35 | NaN | JLBOB-DELY-AVAILABLE-IND-4 | Char | 145 | 145 | 1 | Y | NaN | X | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 36 | NaN | JLBOB-EXPCTD-SHELF-LIFE-5 | Numeric | 146 | 148 | 3 | Y | NaN | 9(3) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 37 | NaN | JLBOB-DELY-AVAILABLE-IND-5 | Char | 149 | 149 | 1 | Y | NaN | X | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 38 | NaN | JLBOB-EXPCTD-SHELF-LIFE-6 | Numeric | 150 | 152 | 3 | Y | NaN | 9(3) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 39 | NaN | JLBOB-DELY-AVAILABLE-IND-6 | Char | 153 | 153 | 1 | Y | NaN | X | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 40 | NaN | JLBOB-EXPCTD-SHELF-LIFE-7 | Numeric | 154 | 156 | 3 | Y | NaN | 9(3) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 41 | NaN | JLBOB-DELY-AVAILABLE-IND-7 | Char | 157 | 157 | 1 | Y | NaN | X | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 42 | NaN | JLBOB-DIR-ORD-GRP | Char | 158 | 159 | 2 | Y | NaN | X(2) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 43 | NaN | JLBOB-NOM-PACK-WEIGHT | Float | 160 | 164 | 5 | Y | NaN | 9(3)V99 | NaN | NaN | NaN | Set to spaces. This is still being evaluated and is subject to change |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail | 44 | NaN | JLBOB-TU-NOTIONAL-WT | Float | 165 | 170 | 6 | Y | NaN | 9(4)V99 | NaN | NaN | NaN | Set to spaces. This is still being evaluated and is subject to change |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Trailer | 1 | NaN | JLBOZ-REC-TYPE | Char | 1 | 1 | 1 | Y | NaN | 9 | NaN | NaN | NaN | Integration layer to set the record type to 9 for trailer |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Trailer | 2 | NaN | JLBOZ-REC-COUNT | Numeric | 2 | 9 | 8 | Y | NaN | 9(8) | NaN | NaN | NaN | Integration layer to put the record count by including header & trailer record |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Trailer | 3 | NaN | FILLER | Char | 10 | 170 | 161 | N | NaN | X(161) | NaN | NaN | NaN | Set to spaces |

## Copybook structure
| File 261 - JLL.IL.JLBPO.PROD.CTRY | File length 170 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 |
| --- | --- | --- | --- | --- | --- | --- |
| \*\*\* GFO Format - Different from UK \*\*\* | NaN | NaN | NaN | NaN | NaN | NaN |
| Field Name | Referenced in CR? | Insync format | Start | Length | COBOL \nFormat | Description |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Header Record | (needs to exist) | G | 1 | 170 | NaN | NaN |
| JLBOA-REC-TYPE | Y | C 1 | 1 | 1 | X | Record type (‘0’ for Header) |
| JLBOA-DATE | Y | C 10 | 2 | 10 | X(10) | Current date when file created. CCYY-MM-DD format.\n |
| FILLER | N | C 159 | 12 | 159 | X(159) | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Detail Record | (needs to exist) | G | 1 | 170 | NaN | NaN |
| JLBOB-REC-TYPE | Y | C 1 | 1 | 1 | X | Record type (‘1’ for Detail) |
| JLBOB-BASE-PRODUCT-NO | Y | Z 9 | 2 | 9 | 9(9) | Base product number |
| JLBOB-BPR-REGN | Y | C 2 | 11 | 2 | X(2) | Country code.  In the UK this either 'UK' or 'RI'.\n\nThis relates to how data is split between UK and ROI.  The situation in the UK is that a product can exist in both the UK and ROI but some fields can have different values between the 2 counties.  For in |
| JLBOB-BASE-PROD-RNGE-CLASS | Y | C 2 | 13 | 2 | X(2) | Range class for the product.\n\nNot relevant for International so supply SPACES. |
| JLBOB-BPR-METRO-RCLASS | Y | C 2 | 15 | 2 | X(2) | Metro range class for the product\n\nNot relevant for International so supply SPACES. |
| JLBOB-STORE-ORDERABLE-IND | Y | C 1 | 17 | 1 | X | Store orderable indicator.\n\nSet to SPACE\n\nThis indicator is used to destock and then restock store/products automatically.  It tends to get used where there is a long term out of stock at a DC.  There has been suggestion that this should be supplied by ra |
| JLBOB-DEVELOPMENT-LINE | Y | C 1 | 18 | 1 | X | Development line.  UK CR currently picks up 'Y' or 'N'.\n\nSet to SPACE.\n\nCR will default to 'N', but I suspect this could well be a field that may need to be manually overridden for certain products. |
| JLBOB-DIAMOND-PROD-IND | Y | C 1 | 19 | 1 | X | Diamond product.  \n\nSet to SPACE.\n\nCurrently supplied by NBS as a space and then set to 'N' in CR.\n\n |
| JLBOB-SRCE-TYPE-IND | Y | C 1 | 20 | 1 | X | Source type indicator.  \n\nSet to SPACE.\n\nUK CR picks up the following: W - Warehouse, D - Direct, B - Both\n\nWhere the indicator is 'B' or 'D' than additional processing is applied to the store orderable indicator to check the product is still orderable fr |
| JLBOB-ORDER-GROUP | Y | C 2 | 21 | 2 | X(2) | Order Group.  \n\nShould be available as a UDA in RMS.\n\nThis solution has still not been worked out so for time being set to SPACES |
| JLBOB-RMS-COMM-HIER | Y | G | 23 | 20 | NaN | The RMS commercial hierarchy.  This is the equivalent of the CR Sub group code.  It is a 20 character string split into 5 fields as follows.  CR will translate this into the appropriate CR 5 character Subgroup code. |
| JLBOB-RMS-DIVISION | Y | Z 4 | 23 | 4 | 9(4) | RMS Division for this product.  Equivalent to the UK Division.  Supply as a number with leading zeroes. |
| JLBOB-RMS-GROUP | Y | Z 4 | 27 | 4 | 9(4) | RMS Group for this product.  Equivalent to the UK Department.  Supply as a number with leading zeroes. |
| JLBOB-RMS-DEPT | Y | Z 4 | 31 | 4 | 9(4) | RMS Department for this product.  Equivalent to the UK Section.  Supply as a number with leading zeroes. |
| JLBOB-RMS-CLASS | Y | Z 4 | 35 | 4 | 9(4) | RMS Class for this product.  Equivalent to the UK Product Group.  Supply as a number with leading zeroes. |
| JLBOB-RMS-SUBCLASS | Y | Z 4 | 39 | 4 | 9(4) | RMS Sub Class for this product.  Equivalent to the UK Sub Group.  Supply as a number with leading zeroes. |
| JLBOB-BASE-PROD-DESCRIPTION | Y | C 48 | 43 | 48 | X(48) | Product description |
| JLBOB-SELL-WT-ITEM-IND | Y | C 1 | 91 | 1 | X | Sell by weight indicator.  Currently assumed to be:\n\nI - Item\nS - Single\nP - Sell by Pack\nW - Sell by Weight\nB - Bird\n\nThe main logic in CR doesn’t appear to differentiate between Item and Single.  Some specific B logic does exist. Seperate Pack and Weigh |
| JLBOB-SALEABLE-EFF-DATE | Y | C 10 | 92 | 10 | X(10) | Sale start date (format ccyy-mm-dd).\n\nCR does use this date in a PFS Sales Extract and as a display field in the online Product mainteneance screen.  The PFS Sales extract doesn't appear to be impacted by removing the Sale Start Date. \n\nSet to SPACES.   \n |
| JLBOB-S-B-W-UNIT-MEASURE | Y | C 4 | 102 | 4 | X(4) | Sell by weight units.  Currently the only values supplied to CR are: SNGL or KG.\n\nCR appears to only check for a specific value of 'KG'.\n\nFor Sell by EACH set to 'SNGL'.  \nFor Sell by Weight, For TURKEY - Set to 'KG', For USA - Set to 'LB'\n\nThe product ma |
| JLBOB-UNIT-SIZE | Y | Z 5, 2 | 106 | 7 | 9(5)V99 | The unit size of the preferred TPND in the format displayed by CR screens, i.e.\n\nFor sale by weight items this field holds the case weight\nFor sell by pack this field holds the contained quantity\nFor all other products it is the unit size\n\nIt seems there |
| JLBOB-LOW-LEVEL-GRP-CD | Y | C 2 | 113 | 2 | X(2) | Set to SPACES.\n\nData Dictionary Description: THE LOW LEVEL GROUP CODE IS USED TO GROUP "LIKE" BASE PRODUCTS WITHIN THE SUBGROUP FOR\nREPORTING PURPOSES. THE DEFINITION OF "LIKE" WILL VARY FROM SUBGROUP TO SUBGROUP DEPENDING ON THE NATURE OF THE PRODUCTS WI |
| JLBOB-BASE-PROD-SEQ-NO | Y | C 3 | 115 | 3 | X(3) | Set to SPACES.\n\nData Dictionary Description: A NUMBER TO SEQUENCE BASE PRODUCTS WITHIN THEIR BASE PRODUCT GROUPING. THE SEQUENCE WILL BE DETERMINED BY THE REPORTING REQUIREMENTS.\n |
| JLBOB-DGRP-CODE | Y | C 3 | 118 | 3 | X(3) | This data item is reliant on the supply authority solution.  Assume to set as SPACES.\n\nData Dictionary Description: A NATIONALLY DEFINED GROUP CONTAINING ONE OR MORE BASE PRODUCTS WHICH WILL BE SUPPLIED TO ANY GIVEN STORE FROM A SINGLE SOURCE OF SUPPLY. |
| JLBOB-MERCH-GRP-CODE | Y | C 3 | 121 | 3 | X(3) | Merchandising code.  Also known as Display Group in International Range.\n\nSet to SPACES\n |
| JLBOB-SUPP-MERCHG-GRP-CODE | Y | C 3 | 124 | 3 | X(3) | Alternative merchandising code - (for Metro stores)\n\nSet to SPACES\n |
| JLBOB-MIN-SHELF-LIFE | Y | Z 3 | 127 | 3 | 9(3) | Minimum shelf life.  If the minimum shelf life is zero and all daily expected shelf live values are zero, then set this field to 999, otherwise set to the minimum shelf life.\n\nNot known at this stage so set to SPACES for time being.  Will need to be resol |
| JLBOB-EXPCTD-SHELF-LIFE-1 | Y | Z 3 | 130 | 3 | 9(3) | Day 1 Expected Shelf Life\n\nNot known at this stage so set to SPACES for time being.  Will need to be resolved longer term. Same applies to the other days. |
| JLBOB-DELY-AVAILABLE-IND-1 | Y | C 1 | 133 | 1 | X | Day 1 Delivery available indicator.\n\nSet to SPACE\n\nCR assumes a value of 'Y' or 'N'.  NBS logic says If ‘X’ set to ‘N’ otherwise set to ‘Y’.  CR will probably default to 'Y'. |
| JLBOB-EXPCTD-SHELF-LIFE-2 | Y | Z 3 | 134 | 3 | 9(3) | Day 2 Expected Shelf Life |
| JLBOB-DELY-AVAILABLE-IND-2 | Y | C 1 | 137 | 1 | X | Day 2 Delivery available indicator.\n\nSet to SPACE\n\nCR assumes a value of 'Y' or 'N'.  NBS logic says If ‘X’ set to ‘N’ otherwise set to ‘Y’.  CR will probably default to 'Y'. |
| JLBOB-EXPCTD-SHELF-LIFE-3 | Y | Z 3 | 138 | 3 | 9(3) | Day 3 Expected Shelf Life |
| JLBOB-DELY-AVAILABLE-IND-3 | Y | C 1 | 141 | 1 | X | Day 3 Delivery available indicator.\n\nSet to SPACE\n\nCR assumes a value of 'Y' or 'N'.  NBS logic says If ‘X’ set to ‘N’ otherwise set to ‘Y’.  CR will probably default to 'Y'. |
| JLBOB-EXPCTD-SHELF-LIFE-4 | Y | Z 3 | 142 | 3 | 9(3) | Day 4 Expected Shelf Life |
| JLBOB-DELY-AVAILABLE-IND-4 | Y | C 1 | 145 | 1 | X | Day 4 Delivery available indicator.\n\nSet to SPACE\n\nCR assumes a value of 'Y' or 'N'.  NBS logic says If ‘X’ set to ‘N’ otherwise set to ‘Y’.  CR will probably default to 'Y'. |
| JLBOB-EXPCTD-SHELF-LIFE-5 | Y | Z 3 | 146 | 3 | 9(3) | Day 5 Expected Shelf Life |
| JLBOB-DELY-AVAILABLE-IND-5 | Y | C 1 | 149 | 1 | X | Day 5 Delivery available indicator.\n\nSet to SPACE\n\nCR assumes a value of 'Y' or 'N'.  NBS logic says If ‘X’ set to ‘N’ otherwise set to ‘Y’.  CR will probably default to 'Y'. |
| JLBOB-EXPCTD-SHELF-LIFE-6 | Y | Z 3 | 150 | 3 | 9(3) | Day 6 Expected Shelf Life |
| JLBOB-DELY-AVAILABLE-IND-6 | Y | C 1 | 153 | 1 | X | Day 6 Delivery available indicator.\n\nSet to SPACE\n\nCR assumes a value of 'Y' or 'N'.  NBS logic says If ‘X’ set to ‘N’ otherwise set to ‘Y’.  CR will probably default to 'Y'. |
| JLBOB-EXPCTD-SHELF-LIFE-7 | Y | Z 3 | 154 | 3 | 9(3) | Day 7 Expected Shelf Life |
| JLBOB-DELY-AVAILABLE-IND-7 | Y | C 1 | 157 | 1 | X | Day 7 Delivery available indicator.\n\nSet to SPACE\n\nCR assumes a value of 'Y' or 'N'.  NBS logic says If ‘X’ set to ‘N’ otherwise set to ‘Y’. |
| JLBOB-DIR-ORD-GRP | Y | C 2 | 158 | 2 | X(2) | Directs order group\n\nSet to SPACES\n\nIn UK this field is usually 'Z' except for bakery products that are not in scope for International.  CR will default this field to 'Z'. |
| JLBOB-NOM-PACK-WEIGHT | Y | Z 3,2 | 160 | 5 | 9(3)V99 | Nominal pack weight of the preferred TPND.\n\nIf  SELL\_BY\_WGT\_ITEM\_IND not = ‘P’  set NOM-PACK-WEIGHT to zero otherwise\n\nCalculate NOM-PACK-WEIGHT as CASE WEIGHT divided by CONTAINMENT QTY\n\nIt seems there is not a concept of preferred TPND in RMS.  If this |
| JLBOB-TU-NOTIONAL-WT | Y | Z 4,2 | 165 | 6 | 9(4)V99 | Notional case weight of the preferred TPND.\n\nIf none exists set to zero.\n\nIt seems there is not a concept of preferred TPND in RMS.  If this is the case, then use the first active TPND for the TPNB that is found in RMS.  This data item is used as a defaul |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Trailer Record | (needs to exist) | NaN | NaN | NaN | NaN | NaN |
| JLBOZ-REC-TYPE | Y | C 1 | 1 | 1 | X | Record type (‘9’ for Trailer) |
| JLBOZ-REC-COUNT | Y | Z 8 | 2 | 8 | 9(8) | Record count including the header and trailer records. |
| FILLER | N | C 161 | 10 | 161 | X(161) | NaN |

## Change History
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 |
| --- | --- | --- | --- |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| Date | Revision | By | Notes |
| 12/06//2006 | Arnab | Debasis Pattanaik | First working version from draft |

## Notes
|
|  |