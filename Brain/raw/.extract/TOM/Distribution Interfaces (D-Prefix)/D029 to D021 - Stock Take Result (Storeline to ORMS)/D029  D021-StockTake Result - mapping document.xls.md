## Mapping
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 | Unnamed: 10 | Unnamed: 11 | Unnamed: 12 | Unnamed: 13 | Unnamed: 14 | Unnamed: 15 | Unnamed: 16 | Unnamed: 17 | Unnamed: 18 | Unnamed: 19 | Unnamed: 20 | Unnamed: 21 | Unnamed: 22 | Unnamed: 23 | Unnamed: 24 | Unnamed: 25 | Unnamed: 26 | Unnamed: 27 | Unnamed: 28 | Unnamed: 29 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | Stock Take Result Mapping(Storeline to ORMS ) | NaN | NaN | NaN | NaN | Version 0.1 | NaN | NaN | NaN | NaN | NaN | NaN | Notes/Issues Key | NaN | NaN | NaN | NaN | NaN | NaN | Key to Mandatory Column | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | General Issues |
| NaN | Source file name:  STKNNNNNN\_TTT\_SSSSSS\_YYYYMMDDHHMMSS.dat | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Business | NaN | NaN | NaN | NaN | NaN | Y | Required | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Store Line contains pack size field - does this mean that the qty is a pack qty or a unit qty? |
| NaN | Source file format: Each field delimited with the character 124 (|) | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Technical | NaN | NaN | NaN | NaN | NaN | N | Optional | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source record structure - transaction header, transaction detail | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Business/Technical | NaN | NaN | NaN | NaN | NaN | C | Conditional - see notes/issues | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Target file name - tsc\_stkupld\_{store number}\_{yyyymmddhhmmss}\_{xxxxxxxxxxxxx}.dat  \*\* {xxx…} to be added by IL | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Maps | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Assumptions on Store Line formats |
| NaN | Target file format: variable length records | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Not mapped/Field Value | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Header and detail have duplicated fields - it is assumed that these duplicated fields contain the same data, and so where duplicate fields exist the detail is used in preference to the header. |
| NaN | Target record structure: file header, file detail, file trailer - positional fixed length fields | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Integration  to use "Target" for mandatory and data validation rules. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | RMS Transaction Unit:  Whole File | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source - Storeline | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Target - ORMS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | RECORD Type | Field No# | Table / Object Name | Field Name / Description | Data Type | Field Start Pos. | Field End Pos. | Field\nSize | Mandatory | Transformation / Condition | Format | Justified (L = Left, R = Right) | Pad Char. | NaN | RECORD Type | Field No# | Table / Object Name | Field Name / Description | Data Type | Field Start Pos. | Field End Pos. | Field Size | Mandatory | Transformation / Condition | Format | Justified (L = Left, R = Right) | Pad Char. | NaN | Notes/Issues |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | File Hdr | 1 | - | File Line Number | Number | 6 | 15 | 10 | Y | NaN | NaN | R | Zero | NaN | - sequential line number in the file to be generated in the IL |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | File Hdr | 2 | - | FileTypeDefination | Char | 16 | 19 | 4 | Y | NaN | STKU | L | Space | NaN | generated by integration layer? |
| NaN | Set Hdr | 2 | NaN | Date of extract | char | NaN | NaN | 8 | Y | NaN | CCYYMMDD | NaN | NaN | NaN | File Hdr | 3 | - | Create Date | Date | 20 | 27 | 8 | Y | NaN | YYYYMMDD | L | Space | NaN | NaN |
| NaN | Set Hdr | 31 | NaN | Time of extract | char | NaN | NaN | 6 | Y | NaN | HHMMSS | NaN | NaN | NaN | File Hdr | 4 | - | Create Time | Time | 28 | 33 | 6 | Y | NaN | HHMMSS | L | Space | NaN | NaN |
| NaN | Set Hdr | 23 | NaN | StocktakeDueDate | char | NaN | NaN | 8 | Y | NaN | CCYYMMDD | NaN | NaN | NaN | File Hdr | 5 | NaN | StockTakeDate | Char | 34 | 47 | 14 | Y | NaN | NaN | R | Zero | NaN | length increased to 8 |
| NaN | Set Hdr | 17 | NaN | RefNo1 | Char | NaN | NaN | 8 | Y | NaN | NaN | NaN | NaN | NaN | File Hdr | 6 | - | CycleCountId | Char | 48 | 55 | 8 | Y | NaN | NaN | R | Zero | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | File Hdr | 7 | - | Location Type | char | 56 | 56 | 1 | Y | S = Store, W = Warehouse | S | L | Space | NaN | generated by integration layer? |
| NaN | Set Hdr | 26 | NaN | Store No. | number | NaN | NaN | 8 | Y | NaN | NaN | NaN | NaN | NaN | File Hdr | 8 | NaN | Location | Number | 57 | 66 | 10 | Y | NaN | NaN | R | Zero | NaN | length increased to 8 |
| NaN | Set Hdr | 1 | NaN | CapturedBy-CreatedBy | Char | NaN | NaN | 1 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 3 | NaN | DelAfterDate | Ccyymmdd | NaN | NaN | 8 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 4 | NaN | DelBeforeDate | Numeric | NaN | NaN | 8 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 5 | NaN | Description | Char | NaN | NaN | 20 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 6 | NaN | DriversName-Courier | Char | NaN | NaN | 30 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 7 | NaN | InvoiceNumber | Char | NaN | NaN | 24 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 8 | NaN | InvoiceTaxTotal | Numeric (7,2) | NaN | NaN | 9 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 9 | NaN | InvoiceTotal | Numeric (7,2) | NaN | NaN | 9 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 10 | NaN | NoOfDetailLines | Numeric | NaN | NaN | 7 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 11 | NaN | OrderDate | Ccyymmdd | NaN | NaN | 8 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 12 | NaN | Order Number /Transaction # | Numeric | NaN | NaN | 14 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 13 | NaN | Order Type/   Count Type | Numeric | NaN | NaN | 8 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 14 | NaN | Original Order number | Numeric | NaN | NaN | 14 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 15 | NaN | ReasonCode | Numeric | NaN | NaN | 4 | N | NaN | 314 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 16 | NaN | RecordType | Char | NaN | NaN | 3 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 18 | NaN | RefNo2 | Char | NaN | NaN | 24 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 19 | NaN | Remarks | Char | NaN | NaN | 60 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 20 | NaN | ReProcessedFlag | Numeric (0/1) | NaN | NaN | 1 | N | if re-extracted 1 else 0 | 0 or 1 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 21 | NaN | SelectionCriteria | NaN | NaN | NaN | NaN | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 22 | NaN | SelectionRange | NaN | NaN | NaN | NaN | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | ` | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 24 | NaN | StoreAddress | Char | NaN | NaN | 100 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |  |
| NaN | Set Hdr | 25 | NaN | StoreName | Char | NaN | NaN | 20 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 27 | NaN | SupplierAddress | Char | NaN | NaN | 64 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 28 | NaN | Supplier Code /       To Store | Char | NaN | NaN | 8 | N | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 29 | NaN | SupplierName | Char | NaN | NaN | 20 | Y | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 30 | NaN | SupplierType | Numeric | NaN | NaN | 1 | Y | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 32 | NaN | TotalQty | Numeric (10,4) | NaN | NaN | 14 | Y | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 33 | NaN | TotalValue | Numeric (7,2) | NaN | NaN | 9 | Y | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 34 | NaN | TransactionDateTime | Ccyymmddhhmmss | NaN | NaN | 14 | Y | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Set Hdr | 35 | NaN | UserName | Char | NaN | NaN | 30 | Y | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | File Dtl | 1 | - | File Line Number | Number | 6 | 15 | 10 | Y | NaN | 000000000n | R | Zero | NaN | - sequential line number in the file to be generated in the IL |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | File Dtl | 2 | - | itemType | char | 16 | 18 | 3 | Y | NaN | ITM | L | Space | NaN | NaN |
| NaN | Set Dtl | 8 | NaN | Item Number | number | NaN | NaN | 14 | Y | NaN | NaN | NaN | NaN | NaN | File Dtl | 3 | - | item | char | 19 | 43 | 25 | Y | NaN | NaN | L | Space | NaN | NaN |
| NaN | Set Dtl | 8 | NaN | CountQty | number | NaN | NaN | 12 | N | NaN | NaN | NaN | NaN | NaN | File Dtl | 4 | - | InventoryQuantity | Number | 44 | 55 | 12 | Y | NaN | NaN | R | Zero | NaN | NaN |
| NaN | Set Dtl | 8 | NaN | Store No. | number | NaN | NaN | 8 | Y | NaN | NaN | NaN | NaN | NaN | File Dtl | 5 | - | InventoryLocationDescription | char | 56 | 85 | 30 | N | NaN | NaN | L | Space | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | File Trlr | 1 | - | File Line number | number | 6 | 15 | 10 | Y | NaN | 000000000n | R | Zero | NaN | Generated by IL |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | File Trlr | 2 | - | Number of File Detail lines | number | 16 | 25 | 10 | Y | NaN | 000000000n | R | Zero | NaN | NaN |

## Target Schema
| 75 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 | Unnamed: 10 | Unnamed: 11 | Unnamed: 12 | Unnamed: 13 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | Target file format is:\n   a single header record, followed by zero or more detail records, followed by a single trailer record\n   the header and trailer records are mandatory\n   the record lengths are fixed for each record type\n   the fields are all fixed length | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Target - ORMS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | RECORD Type | Field No# | Table / Object Name | Field Name / Description | Data Type | Field Start Pos. | Field End Pos. | Field Size | Mandatory | Transformation / Condition | Format | Justified (L = Left, R = Right) | Pad Char. |
| NaN | File Hdr | 1 | - | File Line Number | Number | 6 | 15 | 10 | Y | NaN | NaN | R | Zero |
| NaN | File Hdr | 2 | - | FileTypeDefination | Char | 16 | 19 | 4 | Y | NaN | STKU | L | Space |
| NaN | File Hdr | 3 | - | Create Date | Date | 20 | 27 | 8 | Y | NaN | YYYYMMDD | L | Space |
| NaN | File Hdr | 4 | - | Create Time | Time | 28 | 33 | 6 | Y | NaN | HHMMSS | L | Space |
| NaN | File Hdr | 5 | NaN | StockTakeDate | Char | 34 | 47 | 14 | Y | NaN | NaN | R | Zero |
| NaN | File Hdr | 6 | - | CycleCountId | Char | 48 | 55 | 8 | Y | NaN | NaN | R | Zero |
| NaN | File Hdr | 7 | - | Location Type | char | 56 | 56 | 1 | Y | S = Store, W = Warehouse | S | L | Space |
| NaN | File Hdr | 8 | NaN | Location | Number | 57 | 66 | 10 | Y | NaN | NaN | R | Zero |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | File Dtl | 1 | - | File Line Number | Number | 6 | 15 | 10 | Y | NaN | 000000000n | R | Zero |
| NaN | File Dtl | 2 | - | itemType | char | 16 | 18 | 3 | Y | NaN | ITM | L | Space |
| NaN | File Dtl | 3 | - | item | char | 19 | 43 | 25 | Y | NaN | NaN | L | Space |
| NaN | File Dtl | 4 | - | InventoryQuantity | Number | 44 | 55 | 12 | Y | NaN | NaN | R | Zero |
| NaN | File Dtl | 5 | - | InventoryLocationDescription | char | 56 | 85 | 30 | N | NaN | NaN | L | Space |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | File Trlr | 1 | - | File Line number | number | 6 | 15 | 10 | Y | NaN | 000000000n | R | Zero |
| NaN | File Trlr | 2 | - | Number of File Detail lines | number | 16 | 25 | 10 | Y | NaN | 000000000n | R | Zero |

## Store Line Format
| Unnamed: 0 | Stock Take Result Adjustments | Unnamed: 2 | Unnamed: 3 |
| --- | --- | --- | --- |
| NaN | NaN | NaN | NaN |
| NaN | Field | Type | Length |
| NaN | NaN | NaN | NaN |
| Header | NaN | NaN | NaN |
| 1 | CapturedBy-CreatedBy | Char | 1 |
| 2 | DateOfExtract | Ccyymmdd | 8 |
| 3 | DelAfterDate | Ccyymmdd | 8 |
| 4 | DelBeforeDate | Numeric | 8 |
| 5 | Description | Char | 20 |
| 6 | DriversName-Courier | Char | 30 |
| 7 | InvoiceNumber | Char | 24 |
| 8 | InvoiceTaxTotal | Numeric (7,2) | 9 |
| 9 | InvoiceTotal | Numeric (7,2) | 9 |
| 10 | NoOfDetailLines | Numeric | 7 |
| 11 | OrderDate | Ccyymmdd | 8 |
| 12 | Order Number /Transaction # | Numeric | 14 |
| 13 | Order Type/   Count Type | Numeric | 8 |
| 14 | Original Order number | Numeric | 14 |
| 15 | ReasonCode | Numeric | 4 |
| 16 | RecordType | Char | 3 |
| 17 | RefNo1 | Char | 24 |
| 18 | RefNo2 | Char | 24 |
| 19 | Remarks | Char | 60 |
| 20 | ReProcessedFlag | Numeric (0/1) | 1 |
| 21 | SelectionCriteria | NaN | NaN |
| 22 | SelectionRange | NaN | NaN |
| 23 | StocktakeDueDate | Ccyymmdd | 8 |
| 24 | StoreAddress | Char | 100 |
| 25 | StoreName | Char | 20 |
| 26 | StoreNo | Numeric | 8 |
| 27 | SupplierAddress | Char | 64 |
| 28 | Supplier Code /       To Store | Char | 8 |
| 29 | SupplierName | Char | 20 |
| 30 | SupplierType | Numeric | 1 |
| 31 | TimeOfExtract | Hhmmss | 6 |
| 32 | TotalQty | Numeric (10,4) | 14 |
| 33 | TotalValue | Numeric (7,2) | 9 |
| 34 | TransactionDateTime | Ccyymmddhhmmss | 14 |
| 35 | UserName | Char | 30 |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| Detail | NaN | NaN | NaN |
| 1 | DataTypeOnRecord | NaN | NaN |
| 2 | DateOfExtract | Ccyymmdd | 8 |
| 3 | HOStockTakeRef | NaN | NaN |
| 4 | InvoiceCost | Numeric (6,2) | 8 |
| 5 | InvoiceQty | Numeric (8,4) | 12 |
| 6 | ItemDescription | Char | 60 |
| 7 | ItemNo | Numeric | 14 |
| 8 | LineNo | Numeric | 7 |
| 9 | Location | Char | 20 |
| 10 | OrderQty | Numeric (8,4) | 12 |
| 11 | OrderType | Numeric | 6 |
| 12 | PackSize | Numeric | 5 |
| 13 | ReasonCode | Numeric | 4 |
| 14 | SellingPricePerUOM | Numeric (6,2) | 8 |
| 15 | Sign | + / - | 1 |
| 16 | StoreNo | Numeric | 8 |
| 17 | SupplierItemNo | Char | 24 |
| 18 | Tax % OnCost | Numeric (6,2) | 8 |
| 19 | TimeOfExtract | Hhmmss | 6 |
| 20 | TransactionNo | Numeric | 14 |
| 21 | TransactionQty | Numeric (8,4) | 12 |
| 22 | TRSCostPrice | Numeric (6,2) | 8 |
| 23 | UOMCode | Numeric | 4 |
| 24 | UOMDescription | Char | 20 |

## Store Line notes
| Unnamed: 0 | Unnamed: 1 | STOCK INTERFACE FILES | Unnamed: 3 | Unnamed: 4 |
| --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN |
| 1.0 | File Format | NaN | NaN | NaN |
| NaN | a. | A common file layout will be used for all stock interface files (exports & imports) | NaN | NaN |
| NaN | b. | The files will be in ASCII format | NaN | NaN |
| NaN | c. | Each field is delimited. The character to be used as the delimiter will be determined by the system parameter | NaN | NaN |
| NaN | NaN | “ASCII code for delimiter character in stock interface files”. The default character will be124 (|) | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN |
| 2.0 | File Structure | NaN | NaN | NaN |
| NaN | a. | Each stock interface transaction will be comprised of a header record and several detail records | NaN | NaN |
| NaN | b. | Each interface file will be differentiated by its transaction record type | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | Record Type | Transaction |
| NaN | NaN | Export Files | NaN | NaN |
| NaN | NaN | NaN | 314 | Stock Count Results (Count figures) |
| NaN | NaN | NaN | 315 | Stock Count Results (Differences) |
| NaN | NaN | NaN | 321 | Order Receipts |
| NaN | NaN | NaN | 322 | IBT - IN Receipts |
| NaN | NaN | NaN | 323 | Stock Adjustments (Up & Down) |
| NaN | NaN | NaN | 325 | Return to Supplier |
| NaN | NaN | NaN | 326 | Return to Distribution Centre |
| NaN | NaN | NaN | 327 | Stock Waste |
| NaN | NaN | NaN | 350 | IBT-Out |
| NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | Import Files | NaN | NaN |
| NaN | NaN | NaN | 350 | IBT- IN |
| NaN | NaN | NaN | 351 | PO Deletion |
| NaN | NaN | NaN | 352 | Expected Purchase Orders |
| NaN | NaN | NaN | 358 | Stock Count Request |
| NaN | NaN | NaN | 359 | Stock-on-hand update |
| NaN | NaN | NaN | NaN | NaN |
| 3.0 | File name format | NaN | NaN | NaN |
| NaN | a. | The file name will be in the following format | NaN | NaN |
| NaN | NaN | NaN | STKNNNNNN\_TTT\_SSSSSS\_ccyymmddhhmmss.dat | NaN |
| NaN | NaN | where | NaN | NaN |
| NaN | NaN | NaN | STK - prefix for all Stock interfaces (exports & imports) | NaN |
| NaN | NaN | NaN | NNNNNN - Sequential file number for all record types. (Different sequence for import & export files) | NaN |
| NaN | NaN | NaN | TTT - Record type | NaN |
| NaN | NaN | NaN | SSSSSS - store number | NaN |
| NaN | NaN | NaN | ccyymmddhhmmss - date & time file created | NaN |
| NaN | NaN | NaN | NaN | NaN |
| NaN | b. | Exception for IBT-OUT & IBT-IN, where the same file that is created for the IBT-OUT for the sending | NaN | NaN |
| NaN | NaN | store will be used by the receiving store to import the IBT-IN | NaN | NaN |
| NaN | NaN | NaN | STKNNNNNN\_TTT\_SSSSSS\_RRRRRR\_ccyymmddhhmmss.dat | NaN |
| NaN | NaN | where | NaN | NaN |
| NaN | NaN | NaN | SSSSSS - number of sending store | NaN |
| NaN | NaN | NaN | RRRRRR - number of receiving store | NaN |
| NaN | NaN | NaN | NaN | NaN |
| 4.0 | Paths | NaN | NaN | NaN |
| NaN | a. | Import files must reside in the directory specified by the system parameter “Store\Technical\Interface Parameters\Folder name for Import file" for them to be imported | NaN | NaN |
| NaN | b. | Files extracted for export will be placed in the directory specified by the system parameter “Store \ Technical \ Interface Parameters\Folder name for Export file” | NaN | NaN |

## Change history
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 |
| --- | --- | --- | --- |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| Date | revision | By | Notes |
| 2007-02-12 00:00:00 | 0.1D | Debasis Pattanaik | Draft Version |