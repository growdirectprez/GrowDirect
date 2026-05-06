## Mapping
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 | Unnamed: 10 | Unnamed: 11 | Unnamed: 12 | Unnamed: 13 | Unnamed: 14 | Unnamed: 15 | Unnamed: 16 | Unnamed: 17 | Unnamed: 18 | Unnamed: 19 | Unnamed: 20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | RMS to TIMS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Notes/Issues Key | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source format: Positional Flat File | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Business | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source record structure - Positional fields | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Technical | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source interface: RMS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Business/Technical | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Target File Name: TIMS\_PO\_<YYYYMMDDHH24miss>.txt | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Maps | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Target file format: Pipe Delimited Flat File | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Not mapped/Set Field Value | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Target Record Structure -  Pipe Delimited Fields | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set by Integration Layer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Integration to use "Target" for mandatory and data validation rules. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | Notes: \n1. For TSHIP details \nDirect POs - One PO must have only one shipping location with the location type = 'ST'.\nFor Pick By Line (PBL) - One PO must have a single line in shipping Location type with 'WH' and Quantity type flag = 'S' and rest of records will be one or more line with Quantity type flag = 'A' \nFor Pick By Store (PBS) - One PO must have First line in  shipping Location type with 'WH'  and no further lines\nIf above conditions are not satisfied then, It is an erronious transaction\n2. Source Character set for Turkey is 8859-9, and target character set is UTF-8\n3. Validate record counts and date against FHEAD and FTAIL\n4. Address Information - The data can be truncated with 35 characters (LToR) and send to TIMS interface.\n5. Source file line delimiter is line feed.\n6. PIPE | symbol is field delimiter in target schema. Validation has to happen for every alpha-numeric field of Source file to check for | symbol. If | symbol is found then it has to be replaced with ' ' space while mapping. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Issues: \n1. ITEM in TITEM head in target msg Schema could not be mapped. Is it EAN\_ID from source msg schema? | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Transaction unit: Whole File | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source - RMS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Target - TIMS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | RECORD Type | Field No# | Table / Object Name | Field Name / Description | Data Type | Mandatory | Transformation / Condition | Format | Justified (L = Left, R = Right) | Pad Char. | NaN | RECORD Type | Field No# | Table / Object Name | Field Name / Description | Data Type | Mandatory | Pad Char. | NaN | Notes/Issues |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 1 | NaN | RECTYPE | VARCHAR2(1) | NaN | NaN | NaN | Type of record “H” |
| NaN | TORDR | NaN | NaN | Order change type | Char(2) | NaN | If Order change type = 'NW' then\n“N” – New\nelse if Order change type = 'CH' then\n“C” – Changed | NaN | NaN | NaN | NaN | PO Header | 2 | NaN | ACTION | VARCHAR2(1) | NaN | NaN | NaN | NaN |
| NaN | TSHIP | NaN | NaN | Ship to location | Number(10) | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 3 | NaN | ECONMAG | NUMBER(10) | NaN | NaN | NaN | Shipping location of First line in TSHIP group to be placed here. |
| NaN | TORDR | NaN | NaN | Order number | Number(8) | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 4 | NaN | ECONCOM | NUMBER(8) | NaN | NaN | NaN | NaN |
| NaN | TORDR | NaN | NaN | Supplier | Number(10) | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 5 | NaN | ECOCNUF | NUMBER(10) | NaN | NaN | NaN | NaN |
| NaN | TORDR | NaN | NaN | New order written date / Old order written date | Char(14) | NaN | If Order change type = 'NW' then\n   New Order Written Date - New\nelse if Order change type = 'CH' then\n   Old order written date – Changed | NaN | NaN | NaN | NaN | PO Header | 6 | NaN | ECODCOM | CHAR(8) | NaN | NaN | NaN | First 10 Characters from source field and update the target field. \nDestination Output format (YYYYMMDD) |
| NaN | TORDR | NaN | NaN | New not before date | Char(14) | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 7 | NaN | ECODLIV | CHAR(8) | NaN | NaN | NaN | First 10 Characters from source field and update the target field. \nDestination Output format (YYYYMMDD) |
| NaN | TORDR | NaN | NaN | New order written date | Char(14) | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 8 | NaN | ECODMAJ | CHAR(8) | N | NaN | NaN | First 10 Characters from source field and update the target field. \nDestination Output format (YYYYMMDD) |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 9 | NaN | ECOUTIL | VARCHAR2(6) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | Supplier | SupplierName | Nvarchar(80) | Y | SELECT Supplier.SupplierName \nWHERE Supplier.SupplierID =  :TORDR.Supplier | NaN | NaN | NaN | NaN | PO Header | 10 | NaN | ADRRAIS | CHAR(35) | NaN | NaN | NaN | Common Form Name: TOM.C008ORMS.Schema.Supplier\nInput Parameter: TORDR.Supplier\nOutput field: SupplierName |
| NaN | NaN | NaN | Address | AddrLine1 | Nvarchar(240) | Y | SELECT Address.AddrLine1 \nFROM AddressForSupplierActivity, Address \nWHERE AddressForSupplierActivity.SupplierID = :TORDR.Supplier\nAND AddressForSupplierActivity.AddressID = Address.AddressID\nAND AddressForSupplierActivity.SupplierActivityID = '05' | NaN | NaN | NaN | NaN | PO Header | 11 | NaN | ADRRUE1 | CHAR(35) | NaN | NaN | NaN | Common Form name: TOM.Common.Schema.Address\nInput Parameter: TOM.C008ORMS.Schema.Supplier.AddressID\nOutput field: AddrLine1 |
| NaN | NaN | NaN | Address | AddrLine2 | Nvarchar(240) | Y | SELECT Address.AddrLine2 \nFROM AddressForSupplierActivity, Address \nWHERE AddressForSupplierActivity.SupplierID = :TORDR.Supplier\nAND AddressForSupplierActivity.AddressID = Address.AddressID\nAND AddressForSupplierActivity.SupplierActivityID = '05' | NaN | NaN | NaN | NaN | PO Header | 12 | NaN | ADRRUE2 | CHAR(35) | NaN | NaN | NaN | Common Form name: TOM.Common.Schema.Address\nInput Parameter: TOM.C008ORMS.Schema.Supplier.AddressID\nOutput field: AddrLine2 |
| NaN | NaN | NaN | Address | City | Nvarchar(120) | Y | SELECT Address.City\nFROM AddressForSupplierActivity, Address \nWHERE AddressForSupplierActivity.SupplierID = :TORDR.Supplier\nAND AddressForSupplierActivity.AddressID = Address.AddressID\nAND AddressForSupplierActivity.SupplierActivityID = '05' | NaN | NaN | NaN | NaN | PO Header | 13 | NaN | ADRVILL | CHAR(35) | NaN | NaN | NaN | Common Form name: TOM.Common.Schema.Address\nInput Parameter: TOM.C008ORMS.Schema.Supplier.AddressID\nOutput field: City |
| NaN | NaN | NaN | Address | PostCode | Nvarchar(30) | Y | SELECT Address.PostCode\nFROM AddressForSupplierActivity, Address \nWHERE AddressForSupplierActivity.SupplierID = :TORDR.Supplier\nAND AddressForSupplierActivity.AddressID = Address.AddressID\nAND AddressForSupplierActivity.SupplierActivityID = '05' | NaN | NaN | NaN | NaN | PO Header | 14 | NaN | ADRCODE | CHAR(9) | NaN | NaN | NaN | Common Form name: TOM.Common.Schema.Address\nInput Parameter: TOM.C008ORMS.Schema.Supplier.AddressID\nOutput field: PostCode |
| NaN | NaN | NaN | Address | FaxNumber | Varchar(20) | Y | SELECT Address.FaxNumber\nFROM AddressForSupplierActivity, Address \nWHERE AddressForSupplierActivity.SupplierID = :TORDR.Supplier\nAND AddressForSupplierActivity.AddressID = Address.AddressID\nAND AddressForSupplierActivity.SupplierActivityID = '05' | NaN | NaN | NaN | NaN | PO Header | 15 | NaN | ADRTELC | CHAR(16) | N | NaN | NaN | Common Form name: TOM.Common.Schema.Address\nInput Parameter: TOM.C008ORMS.Schema.Supplier.AddressID\nOutput field: ContactFax |
| NaN | NaN | NaN | Address | PhoneNumber | Varchar(20) | Y | SELECT Address.PhoneNumber\nFROM AddressForSupplierActivity, Address \nWHERE AddressForSupplierActivity.SupplierID = :TORDR.Supplier\nAND AddressForSupplierActivity.AddressID = Address.AddressID\nAND AddressForSupplierActivity.SupplierActivityID = '05' | NaN | NaN | NaN | NaN | PO Header | 16 | NaN | ADRTELP | CHAR(16) | N | NaN | NaN | Common Form name: TOM.Common.Schema.Address\nInput Parameter: TOM.C008ORMS.Schema.Supplier.AddressID\nOutput field: ContactPhone |
| NaN | NaN | NaN | Address | ISOCountryCode | Char(3) | Y | SELECT Address.ISOCountryCode\nFROM AddressForSupplierActivity, Address \nWHERE AddressForSupplierActivity.SupplierID = :TORDR.Supplier\nAND AddressForSupplierActivity.AddressID = Address.AddressID\nAND AddressForSupplierActivity.SupplierActivityID = '05' | NaN | NaN | NaN | NaN | PO Header | 17 | NaN | PARLIBL | CHAR(20) | NaN | NaN | NaN | Common Form name: TOM.Common.Schema.Address\nInput Parameter: TOM.C008ORMS.Schema.Supplier.AddressID\nOutput field: ISOCountryCode |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 18 | NaN | MADRAIS\_COMM | CHAR(35) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 19 | NaN | MADRUE1\_COMM | CHAR(35) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 20 | NaN | MADRUE2\_COMM | CHAR(35) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 21 | NaN | MADVILL\_COMM | CHAR(35) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 22 | NaN | MADCODE\_COMM | CHAR(9) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 23 | NaN | MADTELP\_COMM | CHAR(16) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 24 | NaN | MADTELC\_COMM | CHAR(16) | N | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 25 | NaN | PARLIBL\_COMM | CHAR(20) | N | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 26 | NaN | MADRAIS\_FACT | CHAR(35) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 27 | NaN | MADRUE1\_FACT | CHAR(35) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 28 | NaN | MADRUE2\_FACT | CHAR(35) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 29 | NaN | MADVILL\_FACT | CHAR(35) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 30 | NaN | MADCODE\_FACT | CHAR(9) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 31 | NaN | MADTELP\_FACT | CHAR(16) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 32 | NaN | MADTELC\_FACT | CHAR(16) | N | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 33 | NaN | PARLIBL\_FACT | CHAR(20) | N | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | Store / Warehouse | StoreName / WarehouseName | Nvarchar(150) | Y | If Location type = 'ST' then\n  Locate TSHIP.Ship to location in Store table\n  Where Quantity type flag ='S' and pickup StoreName\nElse if Location type = 'WH' then\n  Locate TSHIP.Ship to location in Warehouse table\n  Where Quantity type flag ='S' and pickup WarehouseName | NaN | NaN | NaN | NaN | PO Header | 34 | NaN | MADRAIS\_LIVR | CHAR(35) | NaN | NaN | NaN | If Location type = 'ST' then\n  Common Form: TOM.Common.Schema.Store\n  Input Parameter: TSHIP.Ship to location WHERE Quantity type flag ='S'\n  Output field: StoreName\nElse if Location type = 'WH' then\n  Common Form: TOM.Common.Schema.Warehouse\n  Input Parameter: TSHIP.Ship to location WHERE Quantity type flag ='S'\n  Output field: WarehouseName |
| NaN | NaN | NaN | Address | AddrLine1 | Nvarchar(240) | Y | If Location type = 'ST' then\n  Locate TSHIP.Ship to location in Store table\n  Where Quantity type flag ='S' and pickup AddressID\n  Locate Store.AddressID in Address table Pickup AddrLine1\nElse if Location type = 'WH' then\n  Locate TSHIP.Ship to location in Warehouse table\n  Where Quantity type flag ='S' and pickup AddressID\n  Locate Warehouse.AddressID in Address table Pickup AddrLine1 | NaN | NaN | NaN | NaN | PO Header | 35 | NaN | MADRUE1\_LIVR | CHAR(35) | NaN | NaN | NaN | If Location type = 'ST' then\n  Common Form: TOM.Common.Schema.Address\n  Input Parameter: TOM.Common.Schema.Store.AddressID\n  Output field: AddrLine1\nElse if Location type = 'WH' then\n  Common Form: TOM.Common.Schema.Address\n  Input Parameter: TOM.Common.Schema.Warehouse.AddressID\n  Output field: AddrLine1 |
| NaN | NaN | NaN | Address | AddrLine2 | Nvarchar(240) | Y | If Location type = 'ST' then\n  Locate TSHIP.Ship to location in Store table\n  Where Quantity type flag ='S' and pickup AddressID\n  Locate Store.AddressID in Address table Pickup AddrLine2\nElse if Location type = 'WH' then\n  Locate TSHIP.Ship to location in Warehouse table\n  Where Quantity type flag ='S' and pickup AddressID\n  Locate Warehouse.AddressID in Address table Pickup AddrLine2 | NaN | NaN | NaN | NaN | PO Header | 36 | NaN | MADRUE2\_LIVR | CHAR(35) | NaN | NaN | NaN | If Location type = 'ST' then\n  Common Form: TOM.Common.Schema.Address\n  Input Parameter: TOM.Common.Schema.Store.AddressID\n  Output field: AddrLine2\nElse if Location type = 'WH' then\n  Common Form: TOM.Common.Schema.Address\n  Input Parameter: TOM.Common.Schema.Warehouse.AddressID\n  Output field: AddrLine2 |
| NaN | NaN | NaN | Address | City | Nvarchar(120) | Y | If Location type = 'ST' then\n  Locate TSHIP.Ship to location in Store table\n  Where Quantity type flag ='S' and pickup AddressID\n  Locate Store.AddressID in Address table Pickup City\nElse if Location type = 'WH' then\n  Locate TSHIP.Ship to location in Warehouse table\n  Where Quantity type flag ='S' and pickup AddressID\n  Locate Warehouse.AddressID in Address table Pickup City | NaN | NaN | NaN | NaN | PO Header | 37 | NaN | MADVILL\_LIVR | CHAR(35) | NaN | NaN | NaN | If Location type = 'ST' then\n  Common Form: TOM.Common.Schema.Address\n  Input Parameter: TOM.Common.Schema.Store.AddressID\n  Output field: City\nElse if Location type = 'WH' then\n  Common Form: TOM.Common.Schema.Address\n  Input Parameter: TOM.Common.Schema.Warehouse.AddressID\n  Output field: City |
| NaN | NaN | NaN | Address | PostCode | Nvarchar(30) | Y | If Location type = 'ST' then\n  Locate TSHIP.Ship to location in Store table\n  Where Quantity type flag ='S' and pickup AddressID\n  Locate Store.AddressID in Address table Pickup PostCode\nElse if Location type = 'WH' then\n  Locate TSHIP.Ship to location in Warehouse table\n  Where Quantity type flag ='S' and pickup AddressID\n  Locate Warehouse.AddressID in Address table Pickup PostCode | NaN | NaN | NaN | NaN | PO Header | 38 | NaN | MADCODE\_LIVR | CHAR(9) | NaN | NaN | NaN | If Location type = 'ST' then\n  Common Form: TOM.Common.Schema.Address\n  Input Parameter: TOM.Common.Schema.Store.AddressID\n  Output field: PostCode\nElse if Location type = 'WH' then\n  Common Form: TOM.Common.Schema.Address\n  Input Parameter: TOM.Common.Schema.Warehouse.AddressID\n  Output field: PostCode |
| NaN | NaN | NaN | Address | PhoneNumber | Nvarchar(20) | Y | If Location type = 'ST' then\n  Locate TSHIP.Ship to location in Store table\n  Where Quantity type flag ='S' and pickup AddressID\n  Locate Store.AddressID in Address table Pickup PhoneNumber\nElse if Location type = 'WH' then\n  Locate TSHIP.Ship to location in Warehouse table\n  Where Quantity type flag ='S' and pickup AddressID\n  Locate Warehouse.AddressID in Address table Pickup PhoneNumber | NaN | NaN | NaN | NaN | PO Header | 39 | NaN | MADTELP\_LIVR | CHAR(16) | NaN | NaN | NaN | If Location type = 'ST' then\n  Common Form: TOM.Common.Schema.Address\n  Input Parameter: TOM.Common.Schema.Store.AddressID\n  Output field: ContactPhone\nElse if Location type = 'WH' then\n  Common Form: TOM.Common.Schema.Address\n  Input Parameter: TOM.Common.Schema.Warehouse.AddressID\n  Output field: ContactPhone |
| NaN | NaN | NaN | Address | FaxNumber | Nvarchar(20) | Y | If Location type = 'ST' then\n  Locate TSHIP.Ship to location in Store table\n  Where Quantity type flag ='S' and pickup AddressID\n  Locate Store.AddressID in Address table Pickup FaxNumber\nElse if Location type = 'WH' then\n  Locate TSHIP.Ship to location in Warehouse table\n  Where Quantity type flag ='S' and pickup AddressID\n  Locate Warehouse.AddressID in Address table Pickup FaxNumber | NaN | NaN | NaN | NaN | PO Header | 40 | NaN | MADTELC\_LIVR | CHAR(16) | N | NaN | NaN | If Location type = 'ST' then\n  Common Form: TOM.Common.Schema.Address\n  Input Parameter: TOM.Common.Schema.Store.AddressID\n  Output field: ContactFax\nElse if Location type = 'WH' then\n  Common Form: TOM.Common.Schema.Address\n  Input Parameter: TOM.Common.Schema.Warehouse.AddressID\n  Output field: ContactFax |
| NaN | NaN | NaN | Address | ISOCountryCode | Char(3) | Y | If Location type = 'ST' then\n  Locate TSHIP.Ship to location in Store table\n  Where Quantity type flag ='S' and pickup AddressID\n  Locate Store.AddressID in Address table Pickup ISOCountryCod\nElse if Location type = 'WH' then\n  Locate TSHIP.Ship to location in Warehouse table\n  Where Quantity type flag ='S' and pickup AddressID\n  Locate Warehouse.AddressID in Address table Pickup ISOCountryCode | NaN | NaN | NaN | NaN | PO Header | 41 | NaN | PARLIBL\_LIVR | CHAR(20) | N | NaN | NaN | If Location type = 'ST' then\n  Common Form: TOM.Common.Schema.Address\n  Input Parameter: TOM.Common.Schema.Store.AddressID\n  Output field: ISOCountryCode\nElse if Location type = 'WH' then\n  Common Form: TOM.Common.Schema.Address\n  Input Parameter: TOM.Common.Schema.Warehouse.AddressID\n  Output field: ISOCountryCode |
| NaN | TSHIP | NaN | NaN | New quantity | Number(12) | NaN | Sum of total in order. | NaN | NaN | NaN | NaN | PO Header | 42 | NaN | DCOCOLI | NUMBER(6) | NaN | NaN | 0.0 | Set to the total sum of all the DCOCOLI (ordered purchase units) within the order |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 43 | NaN | DCOQTEP | NUMBER(6) | NaN | NaN | NaN | Set to 0 |
| NaN | TSHIP, TITEM | NaN | NaN | New quantity, \nPack Size | Number(12)\nNumber(12) | NaN | Sum of total in order. | NaN | NaN | NaN | NaN | PO Header | 44 | NaN | DCOQTEC | NUMBER(11,3) | NaN | NaN | NaN | Set to the total sum of all the DCOCTEC (order selling units) within the order. |
| NaN | TSHIP,\nTSHIP | NaN | NaN | New Quantity,\nCase Weight | Number(12),\nNumber(12) | NaN | Sum of total in order. | NaN | NaN | NaN | NaN | PO Header | 45 | NaN | WEIGHT | NUMBER(11,3) | N | NaN | NaN | Set to the total sum of all ARTPBRU (gross weight) within the order. |
| NaN | TORDR | NaN | NaN | New Comment Description | Char(250) | NaN | Truncate to get first 60 chars for target field. | NaN | NaN | NaN | NaN | PO Header | 46 | NaN | ECOLIGN | CHAR(60) | NaN | NaN | NaN | NaN |
| NaN | TORDR | NaN | NaN | New Comment Description | Char(250) | NaN | Truncate to get second 60 chars for target field. | NaN | NaN | NaN | NaN | PO Header | 47 | NaN | ECOLIG2 | CHAR(60) | NaN | NaN | NaN | NaN |
| NaN | TORDR | NaN | NaN | New Currency Code | Char(3) | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 48 | NaN | ECODEVI | VARCHAR2(3) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 49 | NaN | ECOGLN | NUMBER (13) | N | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 1 | NaN | RECTYPE | CHAR(1) | NaN | NaN | NaN | Type of record 'L' |
| NaN | TITEM | NaN | NaN | Item | Char(25) | NaN | NaN | NaN | L | NaN | NaN | PO Items | 2 | NaN | DCOEAN13 | CHAR(14) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 3 | NaN | DCOPVSA | NUMBER(11,3) | NaN | NaN | NaN | Waiting for Business |
| NaN | TITEM | NaN | NaN | Free Form Description | Char(100) | NaN | NaN | NaN | L | NaN | NaN | PO Items | 4 | NaN | ARTLIBL | CHAR(30) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 5 | NaN | DCOSPCB | NUMBER(4) | NaN | NaN | NaN | Set to 0 |
| NaN | TITEM | NaN | NaN | Pack Size | Number(12) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 6 | NaN | DCOPCB | NUMBER(4) | NaN | NaN | NaN | Divide by 10000 to remove implied decimals |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 7 | NaN | PCBPAL | NUMBER(4) | NaN | NaN | NaN | Set to 0 |
| NaN | TSHIP,\nTSHIP | NaN | NaN | New Quantity,\nCase Weight | Number(12),\nNumber(12) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 8 | NaN | ARTPBRU | NUMBER(8,3) | NaN | NaN | NaN | Filter quantity type "S" TSHIP record for every TITEM for a single TORDR. \n\nNew quantity / 10000  \nmultiplied by Case Weight / 10000\nwhere Quantity type flag = 'S'\ngroup by TITEM.item\n\nRound to 3 decimal places |
| NaN | TSHIP, TITEM | NaN | NaN | New quantity, \nPack Size | Number(12)\nNumber(12) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 9 | NaN | DCOQTEC | NUMBER(9,3) | NaN | NaN | NaN | Filter quantity type "S" TSHIP record for every TITEM for a single TORDR. \n\nNew quantity / 10000\nmultiplied by Pack Size / 10000  \nwhere Quantity type flag = 'S'\ngroup by TITEM.item\n\nRound to 3 decimal places |
| NaN | TITEM | NaN | NaN | Vendor catalog number | Char(30) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 10 | NaN | ARCRCOM | CHAR(13) | N | NaN | NaN | NaN |
| NaN | TITEM | NaN | NaN | New Ref Item | Char(25) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 11 | NaN | EAN\_ID | CHAR(13) | NaN | NaN | NaN | RMS will configure EAN/UPC for New Ref Item |
| NaN | TSHIP | NaN | NaN | New Quantity | Number(12) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 12 | NaN | DCOCOLI | NUMBER(9,3) | NaN | NaN | NaN | Filter quantity type "S" TSHIP record for every TITEM for a single TORDR. \n\nNew quantity / 10000  \nwhere Quantity type flag = 'S'\ngroup by TITEM.item\n\nRound to 3 decimal places |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 13 | NaN | DCOQTEP | NUMBER(9,3) | NaN | NaN | NaN | Set to 0 |
| NaN | NaN | NaN | Item | ItemType | Varchar(6) | NaN | This field value is not populated by the EDIDLORD program which populating the source file for this interface. Workaround needed.\n\nSelect Item.ItemType \nfrom Item \nWhere Item.ItemID =  :TITEM.Item | NaN | NaN | NaN | NaN | PO Items | 14 | NaN | DCOPUT | VARCHACR2(10) | NaN | NaN | NaN | NaN |
| NaN | TITEM | NaN | NaN | Pack Size | Number(12) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 15 | NaN | DCOUAUVC | NUMBER (9,3) | NaN | NaN | NaN | Logically (DCOQTEC / DCOCOLI)\nThis value is directly populated from Pack Size filed. The above formula is not required.\n\n\nDivide by 10000 to remove implied decimals |
| NaN | TSHIP | NaN | NaN | New unit cost | Number(20) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 16 | NaN | DCOPRIX | NUMBER(11,3) | NaN | NaN | NaN | Filter quantity type "S" TSHIP record for every TITEM for a single TORDR. \n\nNew unit cost /10000\nwhere Quantity type flag = 'S'\ngroup by TITEM.item\n\nRound to 3 decimal places |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 17 | NaN | DCOIORD | NUMBER(6) | NaN | NaN | NaN | PO Line Item No is not populated thorugh EDIDLORD process. The sequence Number needs to be generated for each PO line Item from Starting of the PO. The sequence number to be re-initialized to 1 for starting the next PO. |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Store Distribution | 1 | NaN | RECTYPE | CHAR(1) | NaN | NaN | NaN | Type of record 'S'\n\nThis portion will be included once the business clarify the docubts\n\nFor every PBL records the Location allocation records will arear here against TITEM\nwhere Quantity type flag = 'A' |
| NaN | TSHIP | NaN | NaN | Ship to location | Number(10) | NaN | NaN | NaN | NaN | NaN | NaN | PO Store Distribution | 2 | NaN | EDCDSITE | NUMBER(10) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Store Distribution | 3 | NaN | EDCSITLIB | CHAR(35) | NaN | NaN | NaN | To confirmed after discussing with John Jolly |
| NaN | TITEM | NaN | NaN | Item | Char(25) | NaN | NaN | NaN | NaN | NaN | NaN | PO Store Distribution | 4 | NaN | EDCDUAUVC | NUMBER(9,3) | NaN | NaN | NaN | NaN |
| NaN | TSHIP | NaN | NaN | New Quantity | Number(12) | NaN | NaN | NaN | NaN | NaN | NaN | PO Store Distribution | 5 | NaN | EDCDQTEC | NUMBER(9,3) | NaN | NaN | NaN | New Quantity / 10000\n\nRound to 3 decimal places |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Store Distribution | 6 | NaN | EDCDQTUA | NUMBER(9,3) | NaN | NaN | NaN | Set to 0 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Store Distribution | 7 | NaN | EDCDNREQ | NUMBER(8) | N | NaN | NaN | Set to 0 |
| NaN | TORDR | NaN | NaN | New order written date / Old order written date | Char(14) | NaN | NaN | NaN | NaN | NaN | NaN | PO Store Distribution | 8 | NaN | EDCDDCRE | CHAR(8) | N | NaN | NaN | If Order change type = 'NW' then\n   New Order Written Date - New\nelse if Order change type = 'CH' then\n   Old order written date – Changed\n\nFirst 10 Characters from source field and update the target field. Destination Output format (YYYYMMDD) |

## Target Msg Schema
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Target Message Schema | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 |
| --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | Code | Optional | Type | Description |
| NaN | NaN | NaN | PO Header: | NaN | NaN | NaN |
| NaN | NaN | NaN | RECTYPE | NaN | VARCHAR2(1) | Type of record “H” |
| NaN | NaN | NaN | ACTION | NaN | VARCHAR2(1) | PO status |
| NaN | NaN | NaN | NaN | NaN | NaN | “W” – waiting |
| NaN | NaN | NaN | NaN | NaN | NaN | “X” – closed |
| NaN | NaN | NaN | ECONMAG | NaN | NUMBER(5) | site ID (Tesco Shop ID) |
| NaN | NaN | NaN | ECONCOM | NaN | NUMBER(8) | purchase order ID |
| NaN | NaN | NaN | ECOCNUF | NaN | NUMBER(9) | supplier ID |
| NaN | NaN | NaN | ECODCOM | NaN | DATE | purchase order date |
| NaN | NaN | NaN | ECODLIV | NaN | DATE | scheduled delivery date |
| NaN | NaN | NaN | ECODMAJ | Yes | DATE | time updated |
| NaN | NaN | NaN | ECOUTIL | NaN | VARCHAR2(6) | user name |
| NaN | NaN | NaN | ADRRAIS | NaN | VARCHAR2(35) | Supplier - corporate name |
| NaN | NaN | NaN | ADRRUE1 | NaN | VARCHAR2(35) | Supplier - street ( 1 ) |
| NaN | NaN | NaN | ADRRUE2 | NaN | VARCHAR2(35) | Supplier - street ( 2 ) |
| NaN | NaN | NaN | ADRVILL | NaN | VARCHAR2(35) | Supplier – city |
| NaN | NaN | NaN | ADRCODE | NaN | VARCHAR2(9) | Supplier – zipcode |
| NaN | NaN | NaN | ADRTELC | Yes | VARCHAR2(16) | Supplier – fax nr |
| NaN | NaN | NaN | ADRTELP | Yes | VARCHAR2(16) | Supplier - telephone nr |
| NaN | NaN | NaN | PARLIBL | NaN | VARCHAR2(20) | long description – country |
| NaN | NaN | NaN | MADRAIS\_COMM | NaN | VARCHAR2(35) | Site raising order - corporate name |
| NaN | NaN | NaN | MADRUE1\_COMM | NaN | VARCHAR2(35) | Site raising order – street ( 1 ) |
| NaN | NaN | NaN | MADRUE2\_COMM | NaN | VARCHAR2(35) | Site raising order – street ( 2 ) |
| NaN | NaN | NaN | MADVILL\_COMM | NaN | VARCHAR2(35) | Site raising order – city |
| NaN | NaN | NaN | MADCODE\_COMM | NaN | VARCHAR2(9) | Site raising order – zipcode |
| NaN | NaN | NaN | MADTELP\_COMM | Yes | VARCHAR2(16) | Site raising order - telephone nr |
| NaN | NaN | NaN | MADTELC\_COMM | Yes | VARCHAR2(16) | Site raising order - fax nr |
| NaN | NaN | NaN | PARLIBL\_COMM | NaN | VARCHAR2(20) | Site raising order – country |
| NaN | NaN | NaN | MADRAIS\_FACT | NaN | VARCHAR2(35) | Invoice address - corporate name |
| NaN | NaN | NaN | MADRUE1\_FACT | NaN | VARCHAR2(35) | Invoice address - street ( 1 ) |
| NaN | NaN | NaN | MADRUE2\_FACT | NaN | VARCHAR2(35) | Invoice address - street ( 2 ) |
| NaN | NaN | NaN | MADVILL\_FACT | NaN | VARCHAR2(35) | Invoice address – city |
| NaN | NaN | NaN | MADCODE\_FACT | NaN | VARCHAR2(9) | Invoice address – zipcode |
| NaN | NaN | NaN | MADTELP\_FACT | NaN | VARCHAR2(16) | Invoice address - telephone nr |
| NaN | NaN | NaN | MADTELC\_FACT | Yes | VARCHAR2(16) | Invoice address - fax nr |
| NaN | NaN | NaN | PARLIBL\_FACT | Yes | VARCHAR2(20) | Invoice address – country |
| NaN | NaN | NaN | MADRAIS\_LIVR | NaN | VARCHAR2(35) | Delivery address - corporate name |
| NaN | NaN | NaN | MADRUE1\_LIVR | NaN | VARCHAR2(35) | Delivery address – street ( 1 ) |
| NaN | NaN | NaN | MADRUE2\_LIVR | NaN | VARCHAR2(35) | Delivery address – street ( 2 ) |
| NaN | NaN | NaN | MADVILL\_LIVR | NaN | VARCHAR2(35) | Delivery address – city |
| NaN | NaN | NaN | MADCODE\_LIVR | NaN | VARCHAR2(9) | Delivery address - zipcode |
| NaN | NaN | NaN | MADTELP\_LIVR | NaN | VARCHAR2(16) | Delivery address - telephone nr |
| NaN | NaN | NaN | MADTELC\_LIVR | Yes | VARCHAR2(16) | Delivery address - fax nr |
| NaN | NaN | NaN | PARLIBL\_LIVR | Yes | VARCHAR2(20) | Delivery address - country |
| NaN | NaN | NaN | DCOCOLI | NaN | NUMBER | quantity in cartons |
| NaN | NaN | NaN | DCOQTEP | NaN | NUMBER | quantity in pallets |
| NaN | NaN | NaN | DCOQTEC | NaN | NUMBER | quantity ( selling unit ) |
| NaN | NaN | NaN | WEIGHT | Yes | NUMBER | Weight |
| NaN | NaN | NaN | ECOLIGN | NaN | VARCHAR2(60) | Comment |
| NaN | NaN | NaN | ECOLIG2 | NaN | VARCHAR2(60) | Comment |
| NaN | NaN | NaN | ECODEVI | NaN | VARCHAR2(3) | Currency |
| NaN | NaN | NaN | ECOGLN | Yes | NUMBER (13) | GLN ship from (NULL value means default GLN from TIMS will be used) |
| NaN | NaN | NaN | PO Items: | NaN | NaN | NaN |
| NaN | NaN | NaN | RECTYPE | NaN | VARCHAR2(1) | Type of record “L” |
| NaN | NaN | NaN | DCOEAN13 | NaN | VARCHAR2(13) | TPN |
| NaN | NaN | NaN | DCOCINT | NaN | NUMBER(9) | RMS internal ID of article |
| NaN | NaN | NaN | DCOPVSA | NaN | NUMBER(11,3) | net purchase price |
| NaN | NaN | NaN | ARTLIBL | NaN | VARCHAR2(30) | article - long description |
| NaN | NaN | NaN | DCOSPCB | NaN | NUMBER(4) | SKU per sub-carton |
| NaN | NaN | NaN | DCOPCB | NaN | NUMBER(4) | SKU per carton |
| NaN | NaN | NaN | PCBPAL | NaN | NUMBER | Cartons per pallet |
| NaN | NaN | NaN | ARTPBRU | NaN | NUMBER(8,3) | gross weight |
| NaN | NaN | NaN | DCOQTEC | NaN | NUMBER(9,3) | quantity ( selling unit ) |
| NaN | NaN | NaN | ARCRCOM | Yes | VARCHAR2(13) | reorder code, SPN |
| NaN | NaN | NaN | EAN\_ID | NaN | VARCHAR2(13) | Cash register article code, EAN/UPC/GS1 code |
| NaN | NaN | NaN | DCOCOLI | NaN | NUMBER(9,3) | quantity in purchase unit |
| NaN | NaN | NaN | DCOQTEP | NaN | NUMBER(9,3) | ordered quantity (pallets) |
| NaN | NaN | NaN | DCOPUT | NaN | VARCHACH2(10) | Purchase unit name |
| NaN | NaN | NaN | DCOUAUVC | NaN | NUMBER (9,3) | Number of SKU in Purchase unit (=DCOQTEC / DCOCOLI) |
| NaN | NaN | NaN | DCOPRIX | NaN | NUMBER(11,3) | Purchase price |
| NaN | NaN | NaN | DCOIORD | NaN | NUMBER(6) | Original PO line item number |
| NaN | NaN | NaN | PO Store Distribution | NaN | NaN | NaN |
| NaN | NaN | NaN | RECTYPE | NaN | VARCHAR2(1) | Type of record “S” |
| NaN | NaN | NaN | EDCDSITE | NaN | number(5) | destination site |
| NaN | NaN | NaN | EDCSITLIB | NaN | varchar2(35) | name of site |
| NaN | NaN | NaN | EDCDUAUVC | NaN | number(9,3) | Number of SKU/purchase unit |
| NaN | NaN | NaN | EDCDQTEC | NaN | number(9,3) | SKU quantity for the site |
| NaN | NaN | NaN | EDCDQTUA | NaN | number(9,3) | PU quantity for the site |
| NaN | NaN | NaN | EDCDNREQ | Yes | number(8) | destination site order number |
| NaN | NaN | NaN | EDCDDCRE | Yes | Date | creation date of site order |

## Change History
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 |
| --- | --- | --- | --- |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| Date | Revision | By | Notes |
| 2007-05-01 00:00:00 | V1.0 | Supriyo Chakraborty | Andy is working on the unmapped fields |
| 2007-11-01 00:00:00 | V2.0 | Sankar G | Based on Andy's discussion with Business and ITS |
| 26/2/2007 | V3.0 | Sankar G | CR for Line delimiter and new common forms |
| 26/2/2007 | V4.0 | Sankar G | CR for Removing PIPE symbol from Alpha-Numeric filelds |
| 27/02/2007 | V5.0 | Sankar G | Line delimiter set back to Line feed |
| 2007-12-03 00:00:00 | V6.0 | Sankar G | Change the mapping for ISOCountryCode, ItemType |
| 13/3/2007 | V7.0 | Sankar G | Change the mapping for populating the PO line number |
| 14/3/2007 | V8.0 | Sankar G | Change in Supplier Address data fetch through Web-service call |

## Notes
|
|  |