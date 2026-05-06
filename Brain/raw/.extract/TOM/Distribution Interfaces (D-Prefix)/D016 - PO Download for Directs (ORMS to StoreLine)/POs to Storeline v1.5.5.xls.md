## Mapping
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 | Unnamed: 10 | Unnamed: 11 | Unnamed: 12 | Unnamed: 13 | Unnamed: 14 | Unnamed: 15 | Unnamed: 16 | Unnamed: 17 | Unnamed: 18 | Unnamed: 19 | Unnamed: 20 | Unnamed: 21 | Unnamed: 22 | Unnamed: 23 | Unnamed: 24 | Unnamed: 25 | Unnamed: 26 | Unnamed: 27 | Unnamed: 28 | Unnamed: 29 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | PO Download File Mapping | NaN | NaN | NaN | NaN | Version 1.5.5 | NaN | NaN | NaN | NaN | NaN | NaN | Notes/Issues Key | NaN | NaN | NaN | NaN | NaN | NaN | Key to Mandatory Column | NaN | NaN | NaN | NaN | NaN | As it stands this EDI extract will only occur if the supplier is set up for EDI extracts. This restriction could be removed if the extract process if cloned. | NaN | NaN | NaN |
| NaN | Source file name: tsc\_podnld\_{store number}\_{yyyymmddhhmiss}.dat | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Business | NaN | NaN | NaN | NaN | NaN | Y | Required | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source file format: Fixed length field poistion | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Technical | NaN | NaN | NaN | NaN | NaN | N | Optional | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source record structure - FHEAD,TORDR,TITEM,TSHIP,TTAIL, FTAIL | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Business/Technical | NaN | NaN | NaN | NaN | NaN | C | Conditional - see notes/issues | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source interface: tscpodnld | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Maps | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Target File Name: STKNNNNNN\_TTT\_SSSSSS\_YYYYMMDDHHMMSS.dat | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Not mapped/Set Field Value | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Target file format: Variable length records | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set by Integration Layer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Target Record Structure -  fields delimited by character 124 (|), record terminator CR+LF | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Integration  to use "Target" for mandatory and data validation rules. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | FHEAD - one per file\n    TORDR - one per Purchase Order \*\* may be multiple per FHEAD set\n        TITEM - one per item on the PO \*\* may be multiple per TORDR set\n           TSHIP - one per TITEM set\n    TTAIL - one per TORDR set\nFTAIL - one per file | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Detail record count per Header set is based on the number of TITEM records :: Storeline does not support Packs - only SKUs' | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | RMS Transaction unit: TORDR to TTAIL | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source - RMS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Target - Retalix | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | RECORD Type | Field No# | Table / Object Name | Field Name / Description | Data Type | Field Start Pos. | Field End Pos. | Field\nSize | Mandatory | Transformation / Condition | Format | Justified (L = Left, R = Right) | Pad Char. | NaN | RECORD Type | Field No# | Table / Object Name | Field Name / Description | Data Type | Field Start Pos. | Field End Pos. | Field Size | Mandatory | Transformation / Condition | Format | Justified (L = Left, R = Right) | Pad Char. | NaN | Notes/Issues |
| NaN | Ord Hdr | 1 | - | Record descriptor | Char | 1 | 5 | 5 | Y | NaN | TORDR | NaN | NaN | NaN | Set Hdr | 1 | NaN | Type | NaN | NaN | NaN | 1 | Y | NaN | H | NaN | Delimiter | NaN | NaN |
| NaN | File Hdr | 4 | - | Create Date | char | 36 | 43 | 8 | Y | NaN | YYYYMMDD | L | Space | NaN | Set Hdr | 2 | NaN | Date of extract | NaN | NaN | NaN | 8 | Y | NaN | CCYYMMDD | NaN | Delimiter | NaN | NaN |
| NaN | File Hdr | 5 | - | Create Time | char | 44 | 49 | 6 | Y | NaN | HHMMSS | L | Space | NaN | Set Hdr | 3 | NaN | Time of extract | NaN | NaN | NaN | 6 | Y | NaN | HHMMSS | NaN | Delimiter | NaN | NaN |
| NaN | File Hdr | 7 | - | Location | number | 51 | 60 | 10 | Y | NaN | NaN | R | Zero | NaN | Set Hdr | 4 | NaN | Store No.          / From Store | Numeric | NaN | NaN | 8 | Y | NaN | NaN | NaN | Delimiter | NaN | File Size Increased to 8 |
| NaN | Ord Hdr | 5 |  | Order number | number | 28 | 35 | 8 | Y | NaN |  | R | Zero | NaN | Set Hdr | 5 | NaN | Order Number /Transaction # | Numeric | NaN | NaN | 14 | Y | IL to prefix  with leading zeroes | NaN | NaN | Delimiter | NaN | NaN |
| NaN | Ord Hdr | 4 |  | Order change type | char | 26 | 27 | 2 | Y | ‘CH’ (changed) or ‘NW’ (new) | NaN | L | Space | NaN | Set Hdr | 6 | NaN | Record Type | Char | NaN | NaN | 3 | Y | 352 - create/351 - delete | NaN | NaN | Delimiter | NaN | If Order Change Type = 'NW' then Record Type = 352. If Order Change Type='CH'  Then  IL to create and insert header record of record type 351 for that order with no detail records,  and then a header record of Record Type 352 . |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 7 | NaN | Store Name | Char | NaN | NaN | 20 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 8 | NaN | Store Address | Char | NaN | NaN | 100 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | Ord Hdr | 6 |  | Supplier | Number | 36 | 45 | 10 | Y | NaN |  | R | Zero | NaN | Set Hdr | 9 | NaN | Supplier Code /       To Store | Char | NaN | NaN | 8 | Y | source data field is 10 digits with leading zeros, rightmost 8 are to be taken and must preserve any leading zeros. Eg. Source supplier id = 0000153262 -> target supplier id = 00153262 | NaN | NaN | Delimiter | NaN | added transformation rule |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 10 | NaN | Supplier Name | Char | NaN | NaN | 32 | Y | NaN | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 11 | NaN | Supplier Address | Char | NaN | NaN | 64 | N | NaN | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 12 | NaN | Supplier Type | Numeric | NaN | NaN | 1 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | Ord Hdr | 9 |  | New order written date | char | 75 | 88 | 14 | Y |  | YYYYMMDDHHMMSS | NaN | NaN | NaN | Set Hdr | 13 | NaN | Order Date | NaN | NaN | NaN | 8 | Y | NaN | CCYYMMDD | NaN | Delimiter | NaN | NaN |
| NaN | Ord Hdr | 23 |  | New not before date | char | 301 | 314 | 14 | Y |  | YYYYMMDDHHMMSS | L | Space | NaN | Set Hdr | 14 | NaN | Expected Del Date | NaN | NaN | NaN | 8 | Y | NaN | CCYYMMDD | NaN | Delimiter | NaN | Assuming that the business will use Expected Delivery Date.  Validate during End 2 End testing |
| NaN | Ord Hdr | 23 |  | New not before date | char | 301 | 314 | 14 | Y |  | YYYYMMDDHHMMSS | L | Space | NaN | Set Hdr | 15 | NaN | Del After Date | NaN | NaN | NaN | 8 | N | NaN | CCYYMMDD | NaN | Delimiter | NaN | Either use not before/not after OR expected delivery date. Not both! |
| NaN | Ord Hdr | 25 |  | New not after date | char | 329 | 342 | 14 | Y |  | YYYYMMDDHHMMSS | L | Space | NaN | Set Hdr | 16 | NaN | Del Before Date | NaN | NaN | NaN | 8 | N | NaN | CCYYMMDD | NaN | Delimiter | NaN | Either use not before/not after OR expected delivery date. Not both! |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 17 | NaN | Transaction date | NaN | NaN | NaN | 14 | N | Null | CCYYMMDDHHMMSS | NaN | Delimiter | NaN | Leave as null as it is not required |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 18 | NaN | Order Type/   Count Type | Numeric | NaN | NaN | 8 | N | Null | NaN | NaN | Delimiter | NaN | Not used |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 19 | NaN | Invoice Number | Char | NaN | NaN | 24 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 20 | NaN | Label number | Char | NaN | NaN | 24 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 21 | NaN | Ref No 2 | Char | NaN | NaN | 24 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 22 | NaN | Captured by/ Created by | Char | NaN | NaN | 30 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 23 | NaN | Driver's name/Courier | Char | NaN | NaN | 30 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 24 | NaN | Original Order number | Numeric | NaN | NaN | 14 | N | Null | NaN | NaN | Delimiter | NaN | Reason code numeric |
| NaN | Ord Hdr | 36 |  | New comment description | char | 1145 | 1394 | 250 | N | NaN |  | L | Space | NaN | Set Hdr | 25 | NaN | Remarks | Char | NaN | NaN | 60 | N | NaN | truncate to 60 char | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 26 | NaN | Reason Code | Numeric | NaN | NaN | 4 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 27 | NaN | No. of Detail Lines | Numeric | NaN | NaN | 7 | Y | IL Count of The Set Detail lines | NaN | NaN | Delimiter | NaN | Used by Retalix to check the file before processing. Increased to 7, ,mandatory |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 28 | NaN | Total Qty | Numeric (10,4) | NaN | NaN | 14 | N | Sum the Set Detail Order quantity | NaN | NaN | Delimiter | NaN | Used by Retalix to check the file before processing |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 29 | NaN | Total Value | Numeric (7,2) | NaN | NaN | 9 | N | Sum the Set Detail Trs cost price (excl) per UOM | NaN | NaN | Delimiter | NaN | Used by Retalix to check the file before processing |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 30 | NaN | Invoice Total | Numeric (7,2) | NaN | NaN | 9 | N | Null | NaN | NaN | Delimiter | NaN | Leave as null as it is not required |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 31 | NaN | Invoice Tax Total | Numeric (7,2) | NaN | NaN | 9 | N | Null | NaN | NaN | Delimiter | NaN | Leave as null as it is not required |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 32 | NaN | Description | Char | NaN | NaN | 20 | N | Null | NaN | NaN | Delimiter | NaN | Leave as null as it is not required |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Hdr | 33 | NaN | User name | Char | NaN | NaN | 30 | N | Null | NaN | NaN | Delimiter | NaN | Leave as null as it is not required |
| NaN | File Hdr | 1 | - | File Record Type Descriptor | char | 1 | 5 | 5 | Y | NaN | FHEAD | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | File Hdr | 2 | - | File Line Number | number | 6 | 15 | 10 | Y | NaN | 0000000001 | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | File Hdr | 3 | - | File Type Definition | char | 16 | 35 | 20 | Y | NaN | TSCPODNLD\_v1.5 | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | File Hdr | 6 | - | Location Type | char | 50 | 50 | 1 | Y | S = Store, W = Warehouse | S | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 1 | TORDR | Record descriptor | Char | 1 | 5 | 5 | Y | NaN | TORDR | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 2 |  | Line id | Char | 6 | 15 | 10 | Y | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 3 |  | Transaction id | char | 16 | 25 | 10 | Y | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 7 |  | Vendor order id | char | 46 | 60 | 15 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 8 |  | Old order written date | Char | 61 | 74 | 14 | N | NaN | YYYYMMDDHHMMSS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 10 |  | Old Currency Code | Char | 89 | 91 | 3 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 11 |  | New Currency Code | char | 92 | 94 | 3 | Y | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 12 |  | Old Shipment Method of payment | Char | 95 | 96 | 2 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 13 |  | New Shipment Method of Payment | char | 97 | 98 | 2 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 14 |  | Old Transportation Responsibility | Char | 99 | 100 | 2 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 15 |  | New Transportation Responsibility | Char | 101 | 102 | 2 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 16 |  | Old Trans. Resp. Description | char | 103 | 147 | 45 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 17 |  | New Trans. Resp. Description | Char | 148 | 192 | 45 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 18 |  | Old Title Passage Location | Char | 193 | 194 | 2 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 19 |  | New Title Passage Location | char | 195 | 196 | 2 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 20 |  | Old Title Passage Description | char | 197 | 241 | 45 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 21 |  | New Title Passage Description | char | 242 | 286 | 45 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 22 |  | Old not before date | char | 287 | 300 | 14 | N |  | YYYYMMDDHHMMSS | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 24 |  | Old not after date | char | 315 | 328 | 14 | N |  | YYYYMMDDHHMMSS | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 26 |  | Old Purchase type | char | 343 | 348 | 6 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 27 |  | New Purchase type | char | 349 | 354 | 6 | Y | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 28 |  | Backhaul allowance | number | 355 | 374 | 20 | N | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 29 |  | Old terms description | char | 375 | 614 | 240 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 30 |  | New terms description | char | 615 | 854 | 240 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 31 |  | Old pickup date | char | 855 | 868 | 14 | N |  | YYYYMMDDHHMMSS | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 32 |  | New pickup date | char | 869 | 882 | 14 | N |  | YYYYMMDDHHMMSS | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 33 |  | Old ship method | char | 883 | 888 | 6 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 34 |  | New ship method | char | 889 | 894 | 6 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 35 |  | Old comment description | char | 895 | 1144 | 250 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 37 |  | Supplier DUNS number | number | 1395 | 1403 | 9 | N | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Hdr | 38 |  | Supplier DUNS location | number | 1404 | 1407 | 4 | N | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 1 | NaN | Type | NaN | NaN | NaN | 1 | Y | NaN | D | NaN | Delimiter | NaN | NaN |
| NaN | File Hdr | 4 | - | Create Date | char | 409 | 416 | 8 | Y | NaN | YYYYMMDD | L | Space | NaN | Set Dtl | 2 | NaN | Date of extract | NaN | NaN | NaN | 8 | Y | NaN | CCYYMMDD | NaN | Delimiter | NaN | NaN |
| NaN | File Hdr | 5 | - | Create Time | char | 417 | 422 | 6 | Y | NaN | HHMMSS | L | Space | NaN | Set Dtl | 3 | NaN | Time of extract | NaN | NaN | NaN | 6 | Y | NaN | HHMMSS | NaN | Delimiter | NaN | NaN |
| NaN | File Hdr | 7 | - | Location | number | 51 | 60 | 10 | Y | NaN | NaN | R | Zero | NaN | Set Dtl | 4 | NaN | Store No. | Numeric | NaN | NaN | 8 | Y | NaN | NaN | NaN | Delimiter | NaN | Field size Increased to 8 |
| NaN | Ord Hdr | 5 |  | Order number | number | 28 | 35 | 8 | Y | NaN |  | R | Zero | NaN | Set Dtl | 5 | NaN | Order Number /Transaction # | Numeric | NaN | NaN | 14 | Y | NaN | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 6 | NaN | Record Type | Char | NaN | NaN | 3 | Y | NaN | 352 | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 7 | NaN | Line number | Numeric | NaN | NaN | 7 | Y | NaN | 000000n | NaN | Delimiter | NaN | This is the detal line number within the set header. I.e. start from one for each new header. Increased to 7 |
| NaN | Item | 5 |  | Item | char | 32 | 56 | 25 | Y | NaN |  | L | Space | NaN | Set Dtl | 8 | NaN | Item Number | Numeric | NaN | NaN | 14 | Y | If TITEM.Item Number Type = ? Pack then Use TPACK.Item Number | NaN | NaN | Delimiter | NaN | There is a possibility that packs may be ordered in which case TPACK will exist with the break down of items within the pack. In these cases use the rows in TPACK instead of TITEM. The pack id should not be sent to StoreLine |
| NaN | Pack | 11 | NaN | Item | char | 130 | 154 | 25 | Y | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 9 | NaN | Item Description | Char | NaN | NaN | 60 | N | Null | NaN | NaN | Delimiter | NaN | Leave as null as it is not required |
| NaN | Item | 10 | NaN | Vendor catalog number | char | 119 | 148 | 30 | N | NaN |  | L | Space | NaN | Set Dtl | 10 | NaN | Supplier item # / catalogue # | Char | NaN | NaN | 24 | N | Do not map if TPACK exists | NaN | NaN | Delimiter | NaN | Do not map if TPACK exists as this will be the supplier number of the pack and not the item |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 11 | NaN | UOM Code | Numeric | NaN | NaN | 4 | N | NaN | NaN | NaN | Delimiter | NaN | Retalix-This information was sent in the PLU. Do we need to send it again? |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 12 | NaN | UOM Description | Char | NaN | NaN | 20 | N | NaN | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 13 | NaN | Pack size / Ratio | Numeric | NaN | NaN | 5 | Y | NaN | 1 | NaN | Delimiter | NaN | This should always be set to 1 |
| NaN | Shipment | 9 |  | New quantity | number | 90 | 101 | 12 | Y | Changed qty\_ordered  (4 implied decimal places) | Qty should be eaches | R | Zero | NaN | Set Dtl | 14 | NaN | Order Quantity / Sent quantity | Numeric (8,4) | NaN | NaN | 12 | Y | If no corresponding TSHIP for TITEM then zet the qty to zero (0). | NaN | NaN | Delimiter | NaN | Quantity sent to storeline shou be eaches (ref RK13).  18-Nov - added transformation rule |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 15 | NaN | Trs cost price (excl) per UOM | Numeric (6,2) | NaN | NaN | 8 | N | NaN | NaN | NaN | Delimiter | NaN | RMS- 4 decimal places implied, Retalix - 2 Decimal place implied |
| NaN | Shipment | 7 |  | New unit cost | number | 58 | 77 | 20 | Y | New unit cost (4 implied decimal places) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 16 | NaN | Order Type | Numeric | NaN | NaN | 6 | N | Null | NaN | NaN | Delimiter | NaN | Not used |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 17 | NaN | Reference No. | Numeric | NaN | NaN | 9 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 18 | NaN | Transaction Qty / Count qty  / Acknowledged qty | Numeric (8,4) | NaN | NaN | 12 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 19 | NaN | Reason Code | Numeric | NaN | NaN | 4 | N | Null | NaN | NaN | Delimiter | NaN | Reason code numeric |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 20 | NaN | Invoice Qty | Numeric (8,4) | NaN | NaN | 12 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 21 | NaN | Invoice Cost (excl) per UOM | Numeric (6,2) | NaN | NaN | 8 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 22 | NaN | Tax % on cost | Numeric (6,2) | NaN | NaN | 8 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 23 | NaN | Selling Price per UOM | Numeric (6,2) | NaN | NaN | 8 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set Dtl | 24 | NaN | Location | Char | NaN | NaN | 20 | N | Null | NaN | NaN | Delimiter | NaN | NaN |
| NaN | Item | 1 | TITEM | File record descriptor | Char | 1 | 5 | 5 | Y |  | TITEM | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Item | 2 |  | Line id | char | 6 | 15 | 10 | Y | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Item | 3 |  | Transaction id | char | 16 | 25 | 10 | Y | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Item | 4 |  | Item Number Type | char | 26 | 31 | 6 | Y | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Item | 6 |  | Old Ref Item Number type | char | 57 | 62 | 6 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Item | 7 |  | Old Ref Item | char | 63 | 87 | 25 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Item | 8 |  | New Ref Item Number type | char | 88 | 93 | 6 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Item | 9 |  | New Ref Item | char | 94 | 118 | 25 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Item | 11 | NaN | Free Form Description | char | 149 | 248 | 100 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Item | 12 | NaN | Supplier Diff 1 | char | 249 | 328 | 80 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Item | 13 | NaN | Supplier Diff 2 | char | 329 | 408 | 80 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Item | 14 | NaN | Supplier Diff 3 | char | 409 | 488 | 80 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Item | 15 | NaN | Supplier Diff 4 | char | 489 | 568 | 80 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Item | 16 | NaN | Pack Size | number | 569 | 580 | 12 | N | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 1 | TPACK | File record descriptor | char | 1 | 5 | 5 | C |  | TPACK | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | TPACK is an optional record that is only populated if TITEM is a pack. There could be multiple TPACK rows for a given TITEM. |
| NaN | Pack | 2 |  | Line id | char | 6 | 15 | 10 | Y | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 3 |  | Transaction id | char | 16 | 25 | 10 | Y | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 4 |  | Pack id | char | 26 | 50 | 25 | Y | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 5 |  | Inner pack id | char | 51 | 75 | 25 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 6 |  | Pack Quantity | number | 76 | 87 | 12 | Y | NaN | Packitem\_breakout.pack\_item\_qty (4 implied decimal places) | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 7 |  | Component Pack Quantity | number | 88 | 99 | 12 | N | NaN | Packitem\_breakout.comp\_pack\_qty (4 implied decimal places) | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 8 |  | Item Parent Part Quantity | number | 100 | 111 | 12 | N | NaN | Packitem\_breakout.item\_parent\_pt\_qty (4 implied decimal places) | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 9 | NaN | Item Quantity | number | 112 | 123 | 12 | N | NaN | Packitem\_breakout.item\_qty (4 implied decimal places) | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 10 | NaN | Item Number Type | char | 124 | 129 | 6 | Y | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 12 | NaN | Item Number Type | char | 155 | 160 | 6 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 13 | NaN | Ref Item | char | 161 | 185 | 25 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 14 | NaN | VPN | char | 186 | 215 | 30 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 15 | NaN | Supplier Diff 1 | char | 216 | 295 | 80 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 16 | NaN | Supplier Diff 2 | char | 296 | 375 | 80 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 17 | NaN | Supplier Diff 3 | char | 376 | 455 | 80 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 18 | NaN | Supplier Diff 4 | char | 456 | 535 | 80 | NaN | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 19 | NaN | Item Parent | char | 536 | 560 | 25 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 20 | NaN | Pack template | char | 561 | 568 | 8 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Pack | 21 | NaN | Template description | char | 569 | 608 | 40 | N | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 1 | TSHIP | Record type | char | 1 | 5 | 5 | Y | 'TSHIP' | TSHIP | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 2 |  | Line id | char | 6 | 15 | 10 | Y | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 3 |  | Transaction id | char | 16 | 25 | 10 | Y | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 4 |  | Location type | char | 26 | 27 | 2 | Y | ‘ST’ store or ‘WH’ warehouse | ST | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 5 |  | Ship to location | number | 28 | 37 | 10 | Y | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 6 |  | Old unit cost | number | 38 | 57 | 20 | N | Old unit cost (4 implied decimal places) | NaN | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 8 |  | Old quantity | number | 78 | 89 | 12 | N | Old qty\_ordered or qty\_allocated (4 implied decimal places) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 10 |  | Old outstanding quantity | number | 102 | 113 | 12 | N | Old qty\_ordered-qty\_received (4 implied decimal places)(or qty\_allocated-qty transferred, for an allocation) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 11 |  | New outstanding quantity | number | 114 | 125 | 12 | Y | Changed qty\_ordered-qty\_received (4 implied decimal places)(or qty\_allocated-qty\_transferred, for an allocation) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 12 |  | Cancel code | char | 126 | 126 | 1 | N | NaN | NaN | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 13 | NaN | Old cancelled quantity | number | 127 | 138 | 12 | N | Previous quantity cancelled (4 implied decimal places) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 14 | NaN | New cancelled quantity | Number | 139 | 150 | 12 | N | Changed quantity cancelled (4 implied decimal places) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 15 | NaN | Quantity type flag | char | 151 | 151 | 1 | Y | ‘S’hip to ‘A’llocate | NaN | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 16 | NaN | Store or warehouse indicator | char | 152 | 153 | 2 | Y | ‘ST’ (store) or ‘WH’ (warehouse) | NaN | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 17 | NaN | Old x-dock location | number | 154 | 163 | 10 | N | Alloc\_detail location (store or wh) | NaN | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 18 | NaN | New x-dock location | number | 164 | 173 | 10 | N | Alloc\_detail location (store or wh) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 19 | NaN | Case length | number | 174 | 185 | 12 | N | Case length (4 implied decimal places) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 20 | NaN | Case width | number | 186 | 197 | 12 | N | Case width (4 implied decimal places) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 21 | NaN | Case height | number | 198 | 209 | 12 | N | Case height (4 implied decimal places) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 22 | NaN | Case LWH unit of measure | char | 210 | 213 | 4 | N | Case LWH unit of measure |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 23 | NaN | Case weight | number | 214 | 225 | 12 | N | Case weight (4 implied decimal places) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 24 | NaN | Case weight unit of measure | char | 226 | 229 | 4 | N | Case weight unit of measure |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 25 | NaN | Case liquid volume | number | 230 | 241 | 12 | N | Case liquid volume (4 implied decimal places) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 26 | NaN | Case liquid volume unit of measure | char | 242 | 245 | 4 | N | Case liquid volume unit of measure |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 27 | NaN | Location DUNS number | number | 246 | 254 | 9 | N | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 28 | NaN | Location DUNS loc | number | 255 | 258 | 4 | N | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 29 | NaN | New unit cost init | number | 259 | 278 | 20 | N | New unit cost init (4 implied decimal places) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 30 | NaN | Old unit cost init | number | 279 | 298 | 20 | N | Old unit cost init (4 implied decimal places) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Shipment | 31 | NaN | Item/loc discounts | number | 299 | 318 | 20 | N | Item/loc discounts (4 implied decimal places) |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Trlr | 1 | TTAIL | Record type | char | 1 | 5 | 5 | Y | NaN | TTAIL | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Trlr | 2 |  | Line id | char | 6 | 15 | 10 | Y | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Trlr | 3 |  | Transaction id | char | 16 | 25 | 10 | Y | NaN |  | L | Space | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Ord Trlr | 4 |  | no of lines in transaction | number | 26 | 35 | 10 | Y | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | File Trlr | 1 | FTAIL | Record type | char | 1 | 5 | 5 | Y | NaN | FTAIL | L | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | File Trlr | 2 |  | Line id | char | 6 | 15 | 10 | Y | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | File Trlr | 3 |  | no of lines | number | 16 | 25 | 10 | Y | NaN |  | R | Zero | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |

## RMS edidlord-file-format
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 | Unnamed: 10 | Unnamed: 11 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | FHEAD – REQUIRED. File identification, one line per file. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | TORDR – REQUIRED. Order level info, one line per order. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | TITEM – REQUIRED. Item description, multiple lines per order possible. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | TPACK - Optional only exists if packs exist on the order. This holds the Items within the pack. Multiple lines per TITEM possible | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | TSHIP – REQUIRED. Ship to location and quantity, multiple lines per item possible. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | TTAIL – REQUIRED. Order end, one line per order. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | FTAIL – REQUIRED. End of file marker, one line per file. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | Record Name | Field Name | Field Type | NaN | NaN | Size | Mandatory | Default Value/Format | Description | NaN |
| NaN | 1.0 | FHEAD | File Record Type Descriptor | char | 1.0 | 5.0 | 5 | Y | FHEAD | NaN | NaN |
| NaN | 2.0 |  | File Line Number | number | 6.0 | 15.0 | 10 | Y | 0000000001 | NaN | NaN |
| NaN | 3.0 |  | File Type Definition | char | 16.0 | 35.0 | 20 | Y | TSC\_PODNLD | NaN | NaN |
| NaN | 4.0 |  | Create Date | char | 36.0 | 43.0 | 8 | Y | YYYYMMDD | NaN | NaN |
| NaN | 5.0 |  | Create Time | char | 44.0 | 49.0 | 6 | Y | HHMMSS | NaN | NaN |
| NaN | 6.0 |  | Location Type | char | 50.0 | 50.0 | 1 | Y | S | S = Store, W = Warehouse | NaN |
| NaN | 7.0 |  | Location | number | 51.0 | 60.0 | 10 | Y | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | 1.0 | TORDR | Record descriptor | Char | 1.0 | 5.0 | 5 | Y | 'TORDR' | TORDR | NaN |
| NaN | 2.0 |  | Line id | Char | 6.0 | 15.0 | 10 | Y | NaN |  | NaN |
| NaN | 3.0 |  | Transaction id | char | 16.0 | 25.0 | 10 | Y | NaN |  | NaN |
| NaN | 4.0 |  | Order change type | char | 26.0 | 27.0 | 2 | Y | ‘CH’ (changed) or ‘NW’ (new) | NaN | NaN |
| NaN | 5.0 |  | Order number | number | 28.0 | 35.0 | 8 | Y | NaN |  | NaN |
| NaN | 6.0 |  | Supplier | Number | 36.0 | 45.0 | 10 | Y | NaN |  | NaN |
| NaN | 7.0 |  | Vendor order id | char | 46.0 | 60.0 | 15 | N | NaN |  | NaN |
| NaN | 8.0 |  | Old order written date | Char | 61.0 | 74.0 | 14 | N | NaN | yyyymmddhhmmss | NaN |
| NaN | 9.0 |  | New order written date | char | 75.0 | 88.0 | 14 | Y |  | yyyymmddhhmmss | NaN |
| NaN | 10.0 |  | Old Currency Code | Char | 89.0 | 91.0 | 3 | N | NaN |  | NaN |
| NaN | 11.0 |  | New Currency Code | char | 92.0 | 94.0 | 3 | Y | NaN |  | NaN |
| NaN | 12.0 |  | Old Shipment Method of payment | Char | 95.0 | 96.0 | 2 | N | NaN |  | NaN |
| NaN | 13.0 |  | New Shipment Method of Payment | char | 97.0 | 98.0 | 2 | N | NaN |  | NaN |
| NaN | 14.0 |  | Old Transportation Responsibility | Char | 99.0 | 100.0 | 2 | N | NaN |  | NaN |
| NaN | 15.0 |  | New Transportation Responsibility | Char | 101.0 | 102.0 | 2 | N | NaN |  | NaN |
| NaN | 16.0 |  | Old Trans. Resp. Description | char | 103.0 | 147.0 | 45 | N | NaN |  | NaN |
| NaN | 17.0 |  | New Trans. Resp. Description | Char | 148.0 | 192.0 | 45 | N | NaN |  | NaN |
| NaN | 18.0 |  | Old Title Passage Location | Char | 193.0 | 194.0 | 2 | N | NaN |  | NaN |
| NaN | 19.0 |  | New Title Passage Location | char | 195.0 | 196.0 | 2 | N | NaN |  | NaN |
| NaN | 20.0 |  | Old Title Passage Description | char | 197.0 | 241.0 | 45 | N | NaN |  | NaN |
| NaN | 21.0 |  | New Title Passage Description | char | 242.0 | 286.0 | 45 | N | NaN |  | NaN |
| NaN | 22.0 |  | Old not before date | char | 287.0 | 300.0 | 14 | N |  | yyyymmddhhmmss | NaN |
| NaN | 23.0 |  | New not before date | char | 301.0 | 314.0 | 14 | Y |  | yyyymmddhhmmss | NaN |
| NaN | 24.0 |  | Old not after date | char | 315.0 | 328.0 | 14 | N |  | yyyymmddhhmmss | NaN |
| NaN | 25.0 |  | New not after date | char | 329.0 | 342.0 | 14 | Y |  | yyyymmddhhmmss | NaN |
| NaN | 26.0 |  | Old Purchase type | char | 343.0 | 348.0 | 6 | N | NaN |  | NaN |
| NaN | 27.0 |  | New Purchase type | char | 349.0 | 354.0 | 6 | Y | NaN |  | NaN |
| NaN | 28.0 |  | Backhaul allowance | number | 355.0 | 374.0 | 20 | N | NaN |  | NaN |
| NaN | 29.0 |  | Old terms description | char | 375.0 | 614.0 | 240 | N | NaN |  | NaN |
| NaN | 30.0 |  | New terms description | char | 615.0 | 854.0 | 240 | N | NaN |  | NaN |
| NaN | 31.0 |  | Old pickup date | char | 855.0 | 868.0 | 14 | N |  | yyyymmddhhmmss | NaN |
| NaN | 32.0 |  | New pickup date | char | 869.0 | 882.0 | 14 | N |  | yyyymmddhhmmss | NaN |
| NaN | 33.0 |  | Old ship method | char | 883.0 | 888.0 | 6 | N | NaN |  | NaN |
| NaN | 34.0 |  | New ship method | char | 889.0 | 894.0 | 6 | N | NaN |  | NaN |
| NaN | 35.0 |  | Old comment description | char | 895.0 | 1144.0 | 250 | N | NaN |  | NaN |
| NaN | 36.0 |  | New comment description | char | 1145.0 | 1394.0 | 250 | N | NaN |  | NaN |
| NaN | 37.0 |  | Supplier DUNS number | number | 1395.0 | 1403.0 | 9 | N | NaN |  | NaN |
| NaN | 38.0 |  | Supplier DUNS location | number | 1404.0 | 1407.0 | 4 | N | NaN |  | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | 1.0 | TITEM | File record descriptor | Char | 1.0 | 5.0 | 5 | Y |  | TITEM | NaN |
| NaN | 2.0 |  | Line id | char | 6.0 | 15.0 | 10 | Y | NaN |  | NaN |
| NaN | 3.0 |  | Transaction id | char | 16.0 | 25.0 | 10 | Y | NaN |  | NaN |
| NaN | 4.0 |  | Item Number Type | char | 26.0 | 31.0 | 6 | Y | NaN |  | NaN |
| NaN | 5.0 |  | Item | char | 32.0 | 56.0 | 25 | Y | NaN |  | If a TPACK record exists this will be the Pack id. |
| NaN | 6.0 |  | Old Ref Item Number type | char | 57.0 | 62.0 | 6 | N | NaN |  | NaN |
| NaN | 7.0 |  | Old Ref Item | char | 63.0 | 87.0 | 25 | N | NaN |  | NaN |
| NaN | 8.0 |  | New Ref Item Number type | char | 88.0 | 93.0 | 6 | N | NaN |  | NaN |
| NaN | 9.0 |  | New Ref Item | char | 94.0 | 118.0 | 25 | N | NaN |  | NaN |
| NaN | 10.0 | NaN | Vendor catalog number | char | 119.0 | 148.0 | 30 | N | NaN |  | NaN |
| NaN | 11.0 | NaN | Free Form Description | char | 149.0 | 248.0 | 100 | N | NaN |  | NaN |
| NaN | 12.0 | NaN | Supplier Diff 1 | char | 249.0 | 328.0 | 80 | N | NaN |  | NaN |
| NaN | 13.0 | NaN | Supplier Diff 2 | char | 329.0 | 408.0 | 80 | N | NaN |  | NaN |
| NaN | 14.0 | NaN | Supplier Diff 3 | char | 409.0 | 488.0 | 80 | N | NaN |  | NaN |
| NaN | 15.0 | NaN | Supplier Diff 4 | char | 489.0 | 568.0 | 80 | N | NaN |  | NaN |
| NaN | 16.0 | NaN | Pack Size | number | 569.0 | 580.0 | 12 | N | NaN |  | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | 1.0 | TPACK | File record descriptor | char | 1.0 | 5.0 | 5 | Y |  | TPACK | TPACK is an optional record that is only populated if TITEM is a pack. There could be multiple TPACK rows for a given TITEM. |
| NaN | 2.0 |  | Line id | char | 6.0 | 15.0 | 10 | Y | NaN |  | NaN |
| NaN | 3.0 |  | Transaction id | char | 16.0 | 25.0 | 10 | Y | NaN |  | NaN |
| NaN | 4.0 |  | Pack id | char | 26.0 | 50.0 | 25 | Y | NaN |  | NaN |
| NaN | 5.0 |  | Inner pack id | char | 51.0 | 75.0 | 25 | N | NaN |  | NaN |
| NaN | 6.0 |  | Pack Quantity | number | 76.0 | 87.0 | 12 | Y | NaN | Packitem\_breakout.pack\_item\_qty (4 implied decimal places) | NaN |
| NaN | 7.0 |  | Component Pack Quantity | number | 88.0 | 99.0 | 12 | N | NaN | Packitem\_breakout.comp\_pack\_qty (4 implied decimal places) | NaN |
| NaN | 8.0 |  | Item Parent Part Quantity | number | 100.0 | 111.0 | 12 | N | NaN | Packitem\_breakout.item\_parent\_pt\_qty (4 implied decimal places) | NaN |
| NaN | 9.0 | NaN | Item Quantity | number | 112.0 | 123.0 | 12 | N | NaN | Packitem\_breakout.item\_qty (4 implied decimal places) | NaN |
| NaN | 10.0 | NaN | Item Number Type | char | 124.0 | 129.0 | 6 | Y | NaN |  | NaN |
| NaN | 11.0 | NaN | Item | char | 130.0 | 154.0 | 25 | Y | NaN |  | NaN |
| NaN | 12.0 | NaN | Item Number Type | char | 155.0 | 160.0 | 6 | N | NaN |  | NaN |
| NaN | 13.0 | NaN | Ref Item | char | 161.0 | 185.0 | 25 | N | NaN |  | NaN |
| NaN | 14.0 | NaN | VPN | char | 186.0 | 215.0 | 30 | N | NaN |  | NaN |
| NaN | 15.0 | NaN | Supplier Diff 1 | char | 216.0 | 295.0 | 80 | N | NaN |  | NaN |
| NaN | 16.0 | NaN | Supplier Diff 2 | char | 296.0 | 375.0 | 80 | N | NaN |  | NaN |
| NaN | 17.0 | NaN | Supplier Diff 3 | char | 376.0 | 455.0 | 80 | N | NaN |  | NaN |
| NaN | 18.0 | NaN | Supplier Diff 4 | char | 456.0 | 535.0 | 80 | NaN | NaN |  | NaN |
| NaN | 19.0 | NaN | Item Parent | char | 536.0 | 560.0 | 25 | N | NaN |  | NaN |
| NaN | 20.0 | NaN | Pack template | char | 561.0 | 568.0 | 8 | N | NaN |  | NaN |
| NaN | 21.0 | NaN | Template description | char | 569.0 | 608.0 | 40 | N | NaN |  | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | 1.0 | TSHIP | Record type | char | 1.0 | 5.0 | 5 | Y | 'TSHIP' | TSHIP | NaN |
| NaN | 2.0 |  | Line id | char | 6.0 | 15.0 | 10 | Y | NaN |  | NaN |
| NaN | 3.0 |  | Transaction id | char | 16.0 | 25.0 | 10 | Y | NaN |  | NaN |
| NaN | 4.0 |  | Location type | char | 26.0 | 27.0 | 2 | Y | ‘ST’ store or ‘WH’ warehouse | ST | NaN |
| NaN | 5.0 |  | Ship to location | number | 28.0 | 37.0 | 10 | Y | NaN |  | NaN |
| NaN | 6.0 |  | Old unit cost | number | 38.0 | 57.0 | 20 | N | Old unit cost (4 implied decimal places) | NaN | NaN |
| NaN | 7.0 |  | New unit cost | number | 58.0 | 77.0 | 20 | Y | New unit cost (4 implied decimal places) |  | NaN |
| NaN | 8.0 |  | Old quantity | number | 78.0 | 89.0 | 12 | N | Old qty\_ordered or qty\_allocated (4 implied decimal places) |  | NaN |
| NaN | 9.0 |  | New quantity | number | 90.0 | 101.0 | 12 | Y | Changed qty\_ordered  (4 implied decimal places) |  | NaN |
| NaN | 10.0 |  | Old outstanding quantity | number | 102.0 | 113.0 | 12 | N | Old qty\_ordered-qty\_received (4 implied decimal places)(or qty\_allocated-qty transferred, for an allocation) |  | NaN |
| NaN | 11.0 |  | New outstanding quantity | number | 114.0 | 125.0 | 12 | Y | Changed qty\_ordered-qty\_received (4 implied decimal places)(or qty\_allocated-qty\_transferred, for an allocation) |  | NaN |
| NaN | 12.0 |  | Cancel code | char | 126.0 | 126.0 | 1 | N | NaN | NaN | NaN |
| NaN | 13.0 | NaN | Old cancelled quantity | number | 127.0 | 138.0 | 12 | N | Previous quantity cancelled (4 implied decimal places) |  | NaN |
| NaN | 14.0 | NaN | New cancelled quantity | Number | 139.0 | 150.0 | 12 | N | Changed quantity cancelled (4 implied decimal places) |  | NaN |
| NaN | 15.0 | NaN | Quantity type flag | char | 151.0 | 151.0 | 1 | Y | ‘S’hip to ‘A’llocate | NaN | NaN |
| NaN | 16.0 | NaN | Store or warehouse indicator | char | 152.0 | 153.0 | 2 | Y | ‘ST’ (store) or ‘WH’ (warehouse) | NaN | NaN |
| NaN | 17.0 | NaN | Old x-dock location | number | 154.0 | 163.0 | 10 | N | Alloc\_detail location (store or wh) | NaN | NaN |
| NaN | 18.0 | NaN | New x-dock location | number | 164.0 | 173.0 | 10 | N | Alloc\_detail location (store or wh) |  | NaN |
| NaN | 19.0 | NaN | Case length | number | 174.0 | 185.0 | 12 | N | Case length (4 implied decimal places) |  | NaN |
| NaN | 20.0 | NaN | Case width | number | 186.0 | 197.0 | 12 | N | Case width (4 implied decimal places) |  | NaN |
| NaN | 21.0 | NaN | Case height | number | 198.0 | 209.0 | 12 | N | Case height (4 implied decimal places) |  | NaN |
| NaN | 22.0 | NaN | Case LWH unit of measure | char | 210.0 | 213.0 | 4 | N | Case LWH unit of measure |  | NaN |
| NaN | 23.0 | NaN | Case weight | number | 214.0 | 225.0 | 12 | N | Case weight (4 implied decimal places) |  | NaN |
| NaN | 24.0 | NaN | Case weight unit of measure | char | 226.0 | 229.0 | 4 | N | Case weight unit of measure |  | NaN |
| NaN | 25.0 | NaN | Case liquid volume | number | 230.0 | 241.0 | 12 | N | Case liquid volume (4 implied decimal places) |  | NaN |
| NaN | 26.0 | NaN | Case liquid volume unit of measure | char | 242.0 | 245.0 | 4 | N | Case liquid volume unit of measure |  | NaN |
| NaN | 27.0 | NaN | Location DUNS number | number | 246.0 | 254.0 | 9 | N | NaN |  | NaN |
| NaN | 28.0 | NaN | Location DUNS loc | number | 255.0 | 258.0 | 4 | N | NaN |  | NaN |
| NaN | 29.0 | NaN | New unit cost init | number | 259.0 | 278.0 | 20 | N | New unit cost init (4 implied decimal places) |  | NaN |
| NaN | 30.0 | NaN | Old unit cost init | number | 279.0 | 298.0 | 20 | N | Old unit cost init (4 implied decimal places) |  | NaN |
| NaN | 31.0 | NaN | Item/loc discounts | number | 299.0 | 318.0 | 20 | N | Item/loc discounts (4 implied decimal places) |  | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | 1.0 | TTAIL | Record type | char | 1.0 | 5.0 | 5 | Y | 'TTAIL' | TTAIL | NaN |
| NaN | 2.0 |  | Line id | char | 6.0 | 15.0 | 10 | Y | NaN |  | NaN |
| NaN | 3.0 |  | Transaction id | char | 16.0 | 25.0 | 10 | Y | NaN |  | NaN |
| NaN | 4.0 |  | no of lines in transaction | number | 26.0 | 35.0 | 10 | Y | NaN |  | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | 1.0 | FTAIL | Record type | char | 1.0 | 5.0 | 5 | Y | 'FTAIL' | FTAIL | NaN |
| NaN | 2.0 |  | Line id | char | 6.0 | 15.0 | 10 | Y | NaN |  | NaN |
| NaN | 3.0 |  | no of lines | number | 16.0 | 25.0 | 10 | Y | NaN |  | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | A copy of edidlord.pc is going to be taken and changed so that all new and changed appoved orders are sent to StoreLine. All EDI flag checking needs to be removed. ORDREV will need to be run before each call to this new batch so new PO changes are sent out. A different file needs to be created for each receiving store. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |

## Retalix PO Format
| From FS1847\_BO\_Stock\_Interface\_Mapping.xls version 4.0 August 2004 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 | Unnamed: 10 | Unnamed: 11 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | Purchase Order Import File |  | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Field | Type | Length | NaN | NEW PO - Updating of SQL Fields | NaN | NaN | NaN | PO DELETION | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | Rlvnt | Mndt | NaN | NaN | Rlvnt | Mndt | NaN |
| Header | NaN | NaN | NaN | NaN | NaN | NaN | STK\_ORDER\_HDR | NaN | NaN | NaN | STK\_ORDER\_HDR |
| 1 | Type | H | 1 | NaN | H | M | NaN | NaN | H | M | NaN |
| 2 | Date of file extract / creation | Ccyymmdd | 8 | NaN | ^ | M | NaN | NaN | ^ | M | NaN |
| 3 | Time of file extract / creation | Hhmmss | 6 | NaN | ^ | M | NaN | NaN | ^ | M | NaN |
| 4 | Store No.          / From Store | Numeric | 8 | NaN | ^ | M | NaN | NaN | ^ | M | NaN |
| 5 | Order Number /Transaction # | Numeric | 14 | NaN | ^ | M | ORDER\_ID | NaN | ^ | M | ORDER\_ID |
| 6 | Record Type | Char | 3 | NaN | 352 | M | NaN | NaN | 351 | M | NaN |
| 7 | Store Name | Char | 20 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 8 | Store Address | Char | 100 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 9 | Supplier Code /       To Store | Char | 8 | NaN | ^ | M | SUPPLIER\_ID | NaN | ^ | M | SUPPLIER\_ID |
| 10 | Supplier Name | Char | 32 | NaN | ^ | NaN | NaN | NaN | ^ | NaN | NaN |
| 11 | Supplier Address | Char | 64 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 12 | Supplier Type | Numeric | 1 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 13 | Order Date | Ccyymmdd | 8 | NaN | ^ | M | CREATE\_DT | NaN | ^ | M | CREATE\_DT |
| 14 | Expected Del Date | Ccyymmdd | 8 | NaN | ^ | OR | EXP\_DELIVERY\_DT | NaN | NaN | NaN | NaN |
| 15 | Del After Date | Ccyymmdd | 8 | NaN | ^ | NaN | DEL\_AFTER | NaN | NaN | NaN | NaN |
| 16 | Del Before Date | Ccyymmdd | 8 | NaN | ^ | NaN | DEL\_BEFORE | NaN | NaN | NaN | NaN |
| 17 | Transaction date & time | Ccyymmddhhmmss | 14 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 18 | Order Type/   Count Type | Numeric | 8 | NaN | ^ | NaN | TYPE | NaN | NaN | NaN | NaN |
| 19 | Invoice Number | Char | 24 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 20 | Ref No 1 | Char | 24 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 21 | Ref No 2 | Char | 24 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 22 | Captured by/ Created by | Char | 30 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 23 | Driver's name/Courier | Char | 30 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 24 | Original Order number | Numeric | 14 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 25 | Remarks | Char | 60 | NaN | ^ | NaN | REMARKS | NaN | NaN | NaN | NaN |
| 26 | Reason Code | Numeric | 4 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 27 | No. of Detail Lines | Numeric | 7 | NaN | ^ | M | NaN | NaN | 0 | M | NaN |
| 28 | Total Qty | Numeric (10,4) | 14 | NaN | ^ | NaN | NaN | NaN | NaN | NaN | NaN |
| 29 | Total Value | Numeric (7,2) | 9 | NaN | ^ | NaN | NaN | NaN | NaN | NaN | NaN |
| 30 | Invoice Total | Numeric (7,2) | 9 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 31 | Invoice Tax Total | Numeric (7,2) | 9 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 32 | Description | Char | 20 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 33 | User name | Char | 30 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 34 | Re-processed flag (export only) | Numeric (0/1) | 1 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | Additional fields to be updated | NaN | NaN | NaN | ORDER\_STATUS: | 12 - Sent to Supplier | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | ORIGIN: | 0 - Head Office | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | USER\_ID: | 0 - Admin | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Detail | NaN | NaN | NaN | NaN | NaN | NaN | STK\_ORDER\_DTL | NaN | NaN | NaN | NaN |
| 1 | Type | D | 1 | NaN | D | M | NaN | NaN | N | NaN | NaN |
| 2 | Date of extract | Ccyymmdd | 8 | NaN | ^ | M | NaN | NaN | O | NaN | NaN |
| 3 | Time of extract | Hhmmss | 6 | NaN | ^ | M | NaN | NaN | NaN | NaN | NaN |
| 4 | Store No. | Numeric | 8 | NaN | ^ | M | NaN | NaN | D | NaN | NaN |
| 5 | Order Number /Transaction # | Numeric | 14 | NaN | ^ | M | ORDER\_ID | NaN | E | NaN | NaN |
| 6 | Record Type | Char | 3 | NaN | 352 | M | NaN | NaN | T | NaN | NaN |
| 7 | Line number | Numeric | 7 | NaN | ^ | M | LINE\_NO | NaN | A | NaN | NaN |
| 8 | Item Number | Numeric | 14 | NaN | ^ | M | ITEM\_CD | NaN | I | NaN | NaN |
| 9 | Item Description | Char | 60 | NaN | NaN | NaN | NaN | NaN | L | NaN | NaN |
| 10 | Supplier item # / catalogue # | Char | 24 | NaN | ^ | NaN | VND\_ITM\_ID | NaN | NaN | NaN | NaN |
| 11 | UOM Code | Numeric | 4 | NaN | ^ | NaN | NaN | NaN | R | NaN | NaN |
| 12 | UOM Description | Char | 20 | NaN | ^ | NaN | NaN | NaN | E | NaN | NaN |
| 13 | Pack size / Ratio | Numeric | 5 | NaN | ^ | M | UNIT\_CASE | NaN | C | NaN | NaN |
| 14 | Order Quantity / Sent quantity | Numeric (8,4) | 12 | NaN | ^ | M | ORDER\_QTY | NaN | O | NaN | NaN |
| 15 | Trs cost price (excl) per UOM | Numeric (6,2) | 8 | NaN | ^ | NaN | COST\_PRICE &  COST\_UNIT | NaN | R | NaN | NaN |
| 16 | Order Type | Numeric | 6 | NaN | ^ | NaN | ORD\_TYPE | NaN | D | NaN | NaN |
| 17 | Reference No. | Numeric | 9 | NaN | ^ | NaN | ORD\_REF\_NUM | NaN | S | NaN | NaN |
| 18 | Transaction Qty / Count qty  / Acknowledged qty | Numeric (8,4) | 12 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 19 | Reason Code | Numeric | 4 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 20 | Invoice Qty | Numeric (8,4) | 12 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 21 | Invoice Cost (excl) per UOM | Numeric (6,2) | 8 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 22 | Tax % on cost | Numeric (6,2) | 8 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 23 | Selling Price per UOM | Numeric (6,2) | 8 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 24 | Location | Char | 20 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 25 | Sign (Only for 315 & 323) | + / - | 1 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |

## Change History
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 |
| --- | --- | --- | --- |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| Date | revision | By | Notes |
| 2004-07-16 00:00:00 | 1.3 | Rob Viner | Added new Retalix file format. Also put back the pack record. |
| 2004-08-24 00:00:00 | 1.5 | Hywel Llewellyn | Update following review, sign off from Retalix 9th Aug |
| 2004-10-05 00:00:00 | 1.5.2 | Hywel Llewellyn | IL to use "Target" for mandatory and data validation rules.  TPACK records only exist if item is a pack.  Map to  "Expected Delivery Date", validate business rule during end to end testing.  Updated Mandatory flags and field sizes to reflect new Retalix Specs.  See Retalix Notes and Retalix PO format for more information |
| 2004-10-15 00:00:00 | 1.5.3 | Faris Shimali | changes to clarify source output data format and rules for record counting for IL |
| NaN | NaN | NaN | NaN |
| NaN | 1.5.5 | Faris Shimali | Added transformation rule for handling TITEM records without a corresponding TSHIP - indicating that an item was deleted/cancelled from the order |

## Retalix Notes
| Unnamed: 0 | Unnamed: 1 | STOCK INTERFACE FILES | Unnamed: 3 | Unnamed: 4 | Version 5.0 |
| --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN |
| 1.0 | File Format | NaN | NaN | NaN | NaN |
| NaN | a. | A common file layout will be used for all stock interface files (exports & imports) | NaN | NaN | NaN |
| NaN | b. | The files will be in ASCII format | NaN | NaN | NaN |
| NaN | c. | Each field is delimited. The character to be used as the delimiter will be determined by the system parameter | NaN | NaN | NaN |
| NaN | NaN | “ASCII code for delimiter character in stock interface files”. The default character will be124 (|) | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN |
| 2.0 | File Structure | NaN | NaN | NaN | NaN |
| NaN | a. | Each stock interface transaction will be comprised of a header record and several detail records | NaN | NaN | NaN |
| NaN | b. | Each interface file will be differentiated by its transaction record type | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | Record Type | Transaction | NaN |
| NaN | NaN | Export Files | NaN | NaN | NaN |
| NaN | NaN | NaN | 314 | Stock Count Results (Count figures) | NaN |
| NaN | NaN | NaN | 315 | Stock Count Results (Differences) | NaN |
| NaN | NaN | NaN | 321 | Order Receipts | NaN |
| NaN | NaN | NaN | 322 | IBT - IN Receipts | NaN |
| NaN | NaN | NaN | 323 | Stock Adjustments (Up & Down) | NaN |
| NaN | NaN | NaN | 325 | Return to Supplier | NaN |
| NaN | NaN | NaN | 326 | Return to Distribution Centre | NaN |
| NaN | NaN | NaN | 327 | Stock Waste | NaN |
| NaN | NaN | NaN | 350 | IBT-Out | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | Import Files | NaN | NaN | NaN |
| NaN | NaN | NaN | 350 | IBT- IN | NaN |
| NaN | NaN | NaN | 351 | PO Deletion | NaN |
| NaN | NaN | NaN | 352 | Expected Purchase Orders | NaN |
| NaN | NaN | NaN | 358 | Stock Count Request | NaN |
| NaN | NaN | NaN | 359 | Stock-on-hand update | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN |
| 3.0 | File name format | NaN | NaN | NaN | NaN |
| NaN | a. | The file name will be in the following format | NaN | NaN | NaN |
| NaN | NaN | NaN | STKNNNNNN\_TTT\_SSSSSS\_ccyymmddhhmmss.dat | NaN | NaN |
| NaN | NaN | where | NaN | NaN | NaN |
| NaN | NaN | NaN | STK - prefix for all Stock interfaces (exports & imports) | NaN | NaN |
| NaN | NaN | NaN | NNNNNN - Sequential file number for all record types. (Different sequence for import & export files) | NaN | NaN |
| NaN | NaN | NaN | TTT - Record type | NaN | NaN |
| NaN | NaN | NaN | SSSSSS - store number | NaN | NaN |
| NaN | NaN | NaN | ccyymmddhhmmss - date & time file created | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | b. | Exception for IBT-OUT & IBT-IN, where the same file that is created for the IBT-OUT for the sending | NaN | NaN | NaN |
| NaN | NaN | store will be used by the receiving store to import the IBT-IN | NaN | NaN | NaN |
| NaN | NaN | NaN | STKNNNNNN\_TTT\_SSSSSS\_RRRRRR\_ccyymmddhhmmss.dat | NaN | NaN |
| NaN | NaN | where | NaN | NaN | NaN |
| NaN | NaN | NaN | SSSSSS - number of sending store | NaN | NaN |
| NaN | NaN | NaN | RRRRRR - number of receiving store | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN |
| 4.0 | Paths | NaN | NaN | NaN | NaN |
| NaN | a. | Import files must reside in the directory specified by the system parameter “Store\Technical\Interface Parameters\Folder name for Import file" for them to be imported | NaN | NaN | NaN |
| NaN | b. | Files extracted for export will be placed in the directory specified by the system parameter “Store \ Technical \ Interface Parameters\Folder name for Export file” | NaN | NaN | NaN |