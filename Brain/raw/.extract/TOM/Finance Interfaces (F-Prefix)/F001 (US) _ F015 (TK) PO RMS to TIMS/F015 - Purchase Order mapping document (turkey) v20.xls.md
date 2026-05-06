## Mapping
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 | Unnamed: 10 | Unnamed: 11 | Unnamed: 12 | Unnamed: 13 | Unnamed: 14 | Unnamed: 15 | Unnamed: 16 | Unnamed: 17 | Unnamed: 18 | Unnamed: 19 | Unnamed: 20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | RMS to TIMS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Notes/Issues Key | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Business | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source format: Positional Flat File | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Technical | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source record structure - Positional fields | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Business/Technical | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source interface: RMS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Maps | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Target File Name: ? | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Not mapped/Set Field Value | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Target file format: Pipe Delimited Flat File | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set by Integration Layer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Target Record Structure -  Pipe Delimited Fields | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Integration to use "Target" for mandatory and data validation rules. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | Notes: \n1. For TSHIP details \nDirect POs - One PO must have only one shipping location with the location type = 'ST'.\nFor Pick By Line (PBL) - One PO must have a single line in shipping Location type with 'WH' and Quantity type flag = 'S' and rest of records will be one or more line with Quantity type flag = 'A' \nFor Pick By Store (PBS) - One PO must have First line in  shipping Location type with 'WH'  and no further lines\nIf above conditions are not satisfied then, It is an erronious transaction\n2. Source Character set for Turkey is 8859-9, and target character set is UTF-8\n3. Validate record counts and date against FHEAD and FTAIL\n4. Address Information - The data can be truncated with 35 characters (LToR) and send to TIMS interface. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Issues: \n1. ITEM in TITEM head in target msg Schema could not be mapped. Is it EAN\_ID from source msg schema? | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Transaction unit: Whole File | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source - RMS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Target - TIMS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | RECORD Type | Field No# | Table / Object Name | Field Name / Description | Data Type | Mandatory | Transformation / Condition | Format | Justified (L = Left, R = Right) | Pad Char. | NaN | RECORD Type | Field No# | Table / Object Name | Field Name / Description | Data Type | Mandatory | Pad Char. | NaN | Logic |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 1 | NaN | RECTYPE | VARCHAR2(1) | NaN | NaN | NaN | Type of record “H” |
| NaN | TORDR | NaN | NaN | Order change type | Char(2) | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 2 | NaN | ACTION | VARCHAR2(1) | NaN | NaN | NaN | If Order change type = 'NW' then\n“N” – New\nelse if Order change type = 'CH' then\n“C” – Changed |
| NaN | TSHIP | NaN | NaN | Ship to location | Number(10) | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 3 | NaN | ECONMAG | NUMBER(10) | NaN | NaN | NaN | Shipping location of First line in TSHIP group to be placed here. |
| NaN | TORDR | NaN | NaN | Order number | Number(8) | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 4 | NaN | ECONCOM | NUMBER(8) | NaN | NaN | NaN | NaN |
| NaN | TORDR | NaN | NaN | Supplier | Number(10) | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 5 | NaN | ECOCNUF | NUMBER(10) | NaN | NaN | NaN | NaN |
| NaN | TORDR | NaN | NaN | New order written date / Old order written date | Char(14) | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 6 | NaN | ECODCOM | CHAR(8) | NaN | NaN | NaN | If Order change type = 'NW' then\n   New Order Written Date - New\nelse if Order change type = 'CH' then\n   Old order written date – Changed\n\nFirst 10 Characters from source field and update the target field. Destination Output format (YYYYMMDD) |
| NaN | TORDR | NaN | NaN | New not before date | Char(14) | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 7 | NaN | ECODLIV | CHAR(8) | NaN | NaN | NaN | First 10 Characters from source field and update the target field. Destination Output format (YYYYMMDD) |
| NaN | TORDR | NaN | NaN | New order written date | Char(14) | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 8 | NaN | ECODMAJ | CHAR(8) | N | NaN | NaN | First 10 Characters from source field and update the target field. Destination Output format (YYYYMMDD) |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 9 | NaN | ECOUTIL | VARCHAR2(6) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 10 | NaN | ADRRAIS | CHAR(35) | NaN | NaN | NaN | Web Service Call = TOM.Common.Supplier\nMethod Name = GetSupplierDetailsFromID\nInput Parameter = TORDR.Supplier\nOutput\nSupplierName,SupplierStatus, AddressType, PrimaryAddressInd, AddrLine1, AddrLine2, AddrLine3, City, State, ISOCountryCode, PostCode, ContactName, ContactPhone, ContactTelex, ContactFax, ContactEmail, County\nMap the field SupplierName |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 11 | NaN | ADRRUE1 | CHAR(35) | NaN | NaN | NaN | Web Service Call = TOM.Common.Supplier\nMethod Name = GetSupplierDetailsFromID\nInput Parameter = TORDR.Supplier\nMap the output field AddrLine1 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 12 | NaN | ADRRUE2 | CHAR(35) | NaN | NaN | NaN | Web Service Call = TOM.Common.Supplier\nMethod Name = GetSupplierDetailsFromID\nInput Parameter = TORDR.Supplier\nMap the output field AddrLine2 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 13 | NaN | ADRVILL | CHAR(35) | NaN | NaN | NaN | Web Service Call = TOM.Common.Supplier\nMethod Name = GetSupplierDetailsFromID\nInput Parameter = TORDR.Supplier\nMap the output field City |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 14 | NaN | ADRCODE | CHAR(9) | NaN | NaN | NaN | Web Service Call = TOM.Common.Supplier\nMethod Name = GetSupplierDetailsFromID\nInput Parameter = TORDR.Supplier\nMap the output field PostCode |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 15 | NaN | ADRTELC | CHAR(16) | N | NaN | NaN | Web Service Call = TOM.Common.Supplier\nMethod Name = GetSupplierDetailsFromID\nInput Parameter = TORDR.Supplier\nMap the output field ContactFax |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 16 | NaN | ADRTELP | CHAR(16) | N | NaN | NaN | Web Service Call = TOM.Common.Supplier\nMethod Name = GetSupplierDetailsFromID\nInput Parameter = TORDR.Supplier\nMap the output field ContactPhone |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 17 | NaN | PARLIBL | CHAR(20) | NaN | NaN | NaN | Web Service Call = TOM.Common.Supplier\nMethod Name = GetSupplierDetailsFromID\nInput Parameter = TORDR.Supplier\nMap the output field Country |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 18 | NaN | MADRAIS\_COMM | CHAR(35) | NaN | NaN | NaN | Web Service Call = TOM.Common.Supplier\nMethod Name = GetSupplierDetailsFromID\nInput Parameter = TORDR.Supplier\nMap the output field Country |
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
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 34 | NaN | MADRAIS\_LIVR | CHAR(35) | NaN | NaN | NaN | If Location type = 'ST' then\n  Web Service Call = TOM.Common.Store\n  Method Name = GetStoreByStoreID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\n  Output StoreName, StoreClass, District, StoreName10, StoreName3, PricingSourceStore, PricingSourceCurrency, TransferZoneID, ChannelID, StoreFormat, OriginalCurrencyCode, CurrencyCode, Language, StoreManagerName, TotalSquareFeet, SellingSquareFeet, LinearDistance, StockholdingIndex, MallName, DefaultWarehouseID, StopOrderDays, StartOrderDays, IntegratedPOSIndex, DUNSNumber, DUNSLocation,  AddressType, PrimaryAddressInd, AddrLine1, AddrLine2, AddrLine3, City, State, ISOCountryCode, PostCode, ContactName, ContactPhone, ContactTelex, ContactFax, ContactEmail, County\nMap the field StoreName\nElse if Location type = 'WH' then\n  Web Service Call = TOM.Common.Warehouse\n  Method Name =GetWarehouseByWarehouseID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\n  Output WarehouseName, WarehouseNameSecondary, EmailAddress, ReportingOrgHierType, ReportingOrgHierValue, CurrencyCode, ChannelID, StockHoldingInd, BreakPackInd, RedistributionWHInd, DeliveryPolicy, RestrictedInd, ProtectedInd, ForecastWHInd, RoundingSeq, ReplenishableInd, ReplWarehouseLink, ReplSourceOrder, InvestmentBuyInd, IBWarehouseLink, AutoIBClear, DUNSNumber, DUNSLocation, TSFEntityID, FinisherInd, InboundHandlingDays, VWHTier, OrgUnitID, AddressType, PrimaryAddressInd, AddrLine1, AddrLine2, AddrLine3, City, State, ISOCountryCode, PostCode, ContactName, ContactPhone, ContactTelex, ContactFax, ContactEmail, County\nMap the field WarehouseName\n |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 35 | NaN | MADRUE1\_LIVR | CHAR(35) | NaN | NaN | NaN | If Location type = 'ST' then\n  Web Service Call = TOM.Common.Store\n  Method Name = GetStoreByStoreID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\nMap the field AddrLine1\nElse if Location type = 'WH' then\n  Web Service Call = TOM.Common.Warehouse\n  Method Name =GetWarehouseByWarehouseID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\n  Map the field AddrLine1 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 36 | NaN | MADRUE2\_LIVR | CHAR(35) | NaN | NaN | NaN | If Location type = 'ST' then\n  Web Service Call = TOM.Common.Store\n  Method Name = GetStoreByStoreID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\nMap the field AddrLine2\nElse if Location type = 'WH' then\n  Web Service Call = TOM.Common.Warehouse\n  Method Name =GetWarehouseByWarehouseID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\n  Map the field AddrLine2 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 37 | NaN | MADVILL\_LIVR | CHAR(35) | NaN | NaN | NaN | If Location type = 'ST' then\n  Web Service Call = TOM.Common.Store\n  Method Name = GetStoreByStoreID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\nMap the field City\nElse if Location type = 'WH' then\n  Web Service Call = TOM.Common.Warehouse\n  Method Name =GetWarehouseByWarehouseID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\n  Map the field City |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 38 | NaN | MADCODE\_LIVR | CHAR(9) | NaN | NaN | NaN | If Location type = 'ST' then\n  Web Service Call = TOM.Common.Store\n  Method Name = GetStoreByStoreID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\nMap the field City\nElse if Location type = 'WH' then\n  Web Service Call = TOM.Common.Warehouse\n  Method Name =GetWarehouseByWarehouseID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\n  Map the field City |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 39 | NaN | MADTELP\_LIVR | CHAR(16) | NaN | NaN | NaN | If Location type = 'ST' then\n  Web Service Call = TOM.Common.Store\n  Method Name = GetStoreByStoreID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\nMap the field ContactPhone\nElse if Location type = 'WH' then\n  Web Service Call = TOM.Common.Warehouse\n  Method Name =GetWarehouseByWarehouseID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\n  Map the field ContactPhone |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 40 | NaN | MADTELC\_LIVR | CHAR(16) | N | NaN | NaN | If Location type = 'ST' then\n  Web Service Call = TOM.Common.Store\n  Method Name = GetStoreByStoreID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\nMap the field ContactFax\nElse if Location type = 'WH' then\n  Web Service Call = TOM.Common.Warehouse\n  Method Name =GetWarehouseByWarehouseID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\n  Map the field ContactFax |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Header | 41 | NaN | PARLIBL\_LIVR | CHAR(20) | N | NaN | NaN | If Location type = 'ST' then\n  Web Service Call = TOM.Common.Store\n  Method Name = GetStoreByStoreID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\nMap the field County\nElse if Location type = 'WH' then\n  Web Service Call = TOM.Common.Warehouse\n  Method Name =GetWarehouseByWarehouseID\n  Input Parameter = TSHIP.Ship to location WHERE Quantity type flag ='S'\n  Map the field County |
| NaN | TSHIP | NaN | NaN | New quantity | Number(12) | NaN | Sum of total in order. | NaN | NaN | NaN | NaN | PO Header | 42 | NaN | DCOCOLI | NUMBER(6) | NaN | NaN | 0.0 | Set to the total sum of all the DCOCOLI (ordered purchase units) within the order. |
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
| NaN | TSHIP,\nTSHIP | NaN | NaN | New Quantity,\nCase Weight | Number(12),\nNumber(12) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 8 | NaN | ARTPBRU | NUMBER(8,3) | NaN | NaN | NaN | Filter quantity type "S" TSHIP record for every TITEM for a single TORDR. \n\nNew quantity / 10000  \nmultiplied by Case Weight / 10000\nwhere Quantity type flag = 'S'\ngroup by TITEM.item\n\n\nRound to 3 decimal places |
| NaN | TSHIP, TITEM | NaN | NaN | New quantity, \nPack Size | Number(12)\nNumber(12) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 9 | NaN | DCOQTEC | NUMBER(9,3) | NaN | NaN | NaN | Filter quantity type "S" TSHIP record for every TITEM for a single TORDR. \n\nNew quantity / 10000\nmultiplied by Pack Size / 10000  \nwhere Quantity type flag = 'S'\ngroup by TITEM.item\n\nRound to 3 decimal places |
| NaN | TITEM | NaN | NaN | Vendor catalog number | Char(30) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 10 | NaN | ARCRCOM | CHAR(13) | N | NaN | NaN | NaN |
| NaN | TITEM | NaN | NaN | New Ref Item | Char(25) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 11 | NaN | EAN\_ID | CHAR(13) | NaN | NaN | NaN | RMS will configure EAN/UPC for New Ref Item |
| NaN | TSHIP | NaN | NaN | New Quantity | Number(12) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 12 | NaN | DCOCOLI | NUMBER(9,3) | NaN | NaN | NaN | Filter quantity type "S" TSHIP record for every TITEM for a single TORDR. \n\nNew quantity / 10000  \nwhere Quantity type flag = 'S'\ngroup by TITEM.item\n\nRound to 3 decimal places |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 13 | NaN | DCOQTEP | NUMBER(9,3) | NaN | NaN | NaN | Set to 0 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 14 | NaN | DCOPUT | VARCHACR2(10) | NaN | NaN | NaN | Set to spaces |
| NaN | TITEM | NaN | NaN | Pack Size | Number(12) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 15 | NaN | DCOUAUVC | NUMBER (9,3) | NaN | NaN | NaN | Divide by 10000 to remove implied decimals |
| NaN | TSHIP | NaN | NaN | New unit cost | Number(20) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 16 | NaN | DCOPRIX | NUMBER(11,3) | NaN | NaN | NaN | Filter quantity type "S" TSHIP record for every TITEM for a single TORDR. \n\nNew unit cost /10000\nwhere Quantity type flag = 'S'\ngroup by TITEM.item\n\nRound to 3 decimal places |
| NaN | TITEM | NaN | NaN | Line id | Char(10) | NaN | NaN | NaN | NaN | NaN | NaN | PO Items | 17 | NaN | DCOIORD | NUMBER(6) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Store Distribution | 1 | NaN | RECTYPE | CHAR(1) | NaN | NaN | NaN | Type of record 'S'\n\nThis portion will be included once the business clarify the docubts\n\nFor every PBL records the Location allocation records will arear here against TITEM\nwhere Quantity type flag = 'A' |
| NaN | TSHIP | NaN | NaN | Ship to location | Number(10) | NaN | NaN | NaN | NaN | NaN | NaN | PO Store Distribution | 2 | NaN | EDCDSITE | NUMBER(10) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | PO Store Distribution | 3 | NaN | EDCSITLIB | CHAR(35) | NaN | NaN | NaN | To confirmed after discussing with John Jolly |
| NaN | TITEM | NaN | NaN | Item | Char(25) | NaN | NaN | NaN | NaN | NaN | NaN | PO Store Distribution | 4 | NaN | EDCDUAUVC | NUMBER(9,3) | NaN | NaN | NaN | NaN |
| NaN | TSHIP | NaN | NaN | New Quantity | Number(12) | NaN | NaN | NaN | NaN | NaN | NaN | PO Store Distribution | 5 | NaN | EDCDQTEC | NUMBER(9,3) | NaN | NaN | NaN | New Quantity / 10000 |
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

## Notes
|
|  |