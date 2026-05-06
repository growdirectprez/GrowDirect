## Mapping
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 | Unnamed: 10 | Unnamed: 11 | Unnamed: 12 | Unnamed: 13 | Unnamed: 14 | Unnamed: 15 | Unnamed: 16 | Unnamed: 17 | Unnamed: 18 | Unnamed: 19 | Unnamed: 20 | Unnamed: 21 | Unnamed: 22 | Unnamed: 23 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | ORWMS/ORMS to TIMS | NaN | NaN | NaN | NaN | Version 1.0.0 | NaN | NaN | NaN | NaN | NaN | NaN | Notes/Issues Key | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Business | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source format: XML File | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Technical | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source record structure - XML Hierarchial Structure | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Business/Technical | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source interface: ORWMS/ORMS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Maps | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Target File Name: ? | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Not mapped/Set Field Value | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Target file format: Pipe Delimited Flat File | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Set by Integration Layer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Target Record Structure -  Delimited fields | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Integration to use "Target" for mandatory and data validation rules. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Issues: \n1. Currency information could not be mapped.\n2. Qty UOM need to be passed on to TIMS.\n3. Supplier ID is not coming from RWMS. How TIMS will send the GRN to the right supplier?\n4. VAT Information is not coming from RWMS.\n5. PONO and DOCNO are both NUMBER(8). The source fields are bigger than target field. In that case how the fields will be truncated?\n6. The source data type for PONO is varchar2. How the conversion will occur? | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Notes:\n1) TIMS:- Character Set accepted by TIMS is UTF-8\n2) In  the Source schema the hierachy will follow as below\nReceiptDesc-> Receipt-> ReceiptDtl.  Another detail ReceiptCartonDtl followed by Receipt hierachy will be ignored. \nReceiptDtl block of the envelop carries the Receipt\_nbr. Receipt Block carries the PO\_nbr.\nIn the target schema the header record will carry the PO Number and Receiprt Number.  The break of the beader record whenever the Po no against Receipt No changes Or the Po Number itself change. | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Transaction unit: Whole File | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Source - ORWMS/ORMS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Target - TIMS | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | RECORD Type | Field No# | Table / Object Name | Field Name / Description | Data Type | Field Start Pos. | Field End Pos. | Field\nSize | Mandatory | Transformation / Condition | Format | Justified (L = Left, R = Right) | Pad Char. | NaN | RECORD Type | Field No# | Table / Object Name | Field Name / Description | Data Type | Mandatory | Pad Char. | NaN | Notes/Issues |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 1 | NaN | NOT | VARCHAR2(1) | NaN | NaN | NaN | set to 'H' |
| NaN | ReceiptDtl | NaN | NaN | receipt\_nbr | Number(9) | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 2 | NaN | DOCNO | NUBMER(8) | NaN | NaN | NaN | RMS Receipt No |
| NaN | ReceiptDtl | NaN | NaN | receipt\_date | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 3 | NaN | DATETIME | DATE YYYYMMDDhhmmss | NaN | NaN | NaN | RMS Receipt Name |
| NaN | Receipt | NaN | NaN | po\_nbr | Varchar2(10) | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 4 | NaN | PONO | NUMBER(8) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 5 | NaN | PODATE | DATE YYYYMMDDhhmmss | NaN | NaN | NaN | NaN |
| NaN | ReceiptDtl | NaN | NaN | receipt\_nbr | Number(9) | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 6 | NaN | GRNNO | VARCHAR2(15) | NaN | NaN | NaN | No GRN No comes from RWMS.  \nSet to Null |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 7 | NaN | DLVDATE | DATE | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 8 | NaN | RETNO | NUMBER(8) | NaN | NaN | NaN | Set to Null |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 9 | NaN | RETDATE | DATE | NaN | NaN | NaN | Set to Null |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 10 | NaN | SUPPID | NUMBER(9) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 11 | NaN | SITEINV | NUMBER(5) | NaN | NaN | NaN | NaN |
| NaN | Receipt | NaN | NaN | dc\_dest\_id | varchar2(10) | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 12 | NaN | SITEDLV | NUMBER(9) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 13 | NaN | PAYDATE | DATE | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 14 | NaN | VEHICLE | VARCHAR2(10) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 15 | NaN | STAMP | VARCHAR2(10) | NaN | NaN | NaN | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 16 | NaN | POSITIVE | NUMBER(1) | NaN | NaN | NaN | Set to '1' |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Sum (unit\_qty) | NaN | NaN | NaN | NaN | VRN Header | 17 | NaN | TOTALQTY | NUMBER(11,3) | NaN | NaN | NaN | Sum (all unit\_qty) |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Header | 18 | NaN | CURRENCY | VARCHAR2(3) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Items | 1 | NaN | EAN | VARCHAR2(13) | NaN | NaN | NaN | NaN |
| NaN | ReceiptDtl | NaN | NaN | Item\_id | Varchar2(25) | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Items | 2 | NaN | TPN | VARCHAR2(13) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Items | 3 | NaN | SPN | VARCHAR2(13) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Items | 4 | NaN | STATNO | VARCHAR2(30) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Items | 5 | NaN | CUSTOMS | VARCHAR2(30) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Items | 6 | NaN | DESCRIPTION | VARCHAR2(35) | NaN | NaN | NaN | NaN |
| NaN | ReceiptDtl | NaN | NaN | shipped\_qty | Number(12) | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Items | 7 | NaN | QTYORDER | NUBMER(11,3) | NaN | NaN | NaN | NaN |
| NaN | ReceiptDtl | NaN | NaN | unit\_qty | Number(12) | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Items | 8 | NaN | QTYRECVD | NUMBER(11,3) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Items | 9 | NaN | CATPRICE | NUMBER(11,3) | NaN | NaN | NaN | NaN |
| NaN | ReceiptDtl | NaN | NaN | unit\_cost | Number(20) | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Items | 10 | NaN | NETPRICE | NUMBER(11,3) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Items | 11 | NaN | VATRATE | NUMBER(6,3) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Items | 12 | NaN | UNIT | VARCHAR2(3) | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | VRN Items | 13 | NaN | VATCODE | VARCHAR2(1) | NaN | NaN | NaN | NaN |

## Target Msg Schema
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 |
| --- | --- | --- | --- |
| NaN | NaN | NaN | NaN |
| Name | Optional | Type | Description |
| VRN Header | NaN | NaN | NaN |
| NOT | NaN | VARCHAR2(1) | Type of record “H” |
| DOCNO | NaN | NUBMER(8) | RMS VRN number. |
| DATETIME | NaN | DATE YYYYMMDDhhmmss | Document creation (original) |
| PONO | NaN | NUMBER(8) | Reference to associated PO |
| PODATE | NaN | DATE YYYYMMDDhhmmss | Date of purchase order |
| GRNNO | NaN | VARCHAR2(15) | ? |
| DLVDATE | NaN | DATE | Requested delivery date. (from PO) |
| RETNO | Y | NUMBER(8) | empty |
| RETDATE | Y | DATE | empty |
| SUPPID | NaN | NUMBER(9) | Supplier ID |
| SITEINV | NaN | NUMBER(5) | RMS ID of Tesco invoicing site |
| SITEDLV | NaN | NUMBER(9) | RMS ID of Tesco delivery site |
| PAYDATE | NaN | DATE | Date of payment |
| VEHICLE | NaN | VARCHAR2(10) | Vehicle registration number |
| STAMP | NaN | VARCHAR2(10) | Stamp number (advice number) (blank) |
| POSITIVE | NaN | NUMBER(1) | 1 |
| TOTALQTY | NaN | NUMBER(11,3) | Total quantity of VRN in SKU units |
| CURRENCY | NaN | VARCHAR2(3) | VRN currency |
| VRN Items | NaN | NaN | NaN |
| EAN | NaN | VARCHAR2(13) | EAN/GS2/BARCODE If there is more than one EAN, this will be the first Active EAN that is found. |
| TPN | NaN | VARCHAR2(13) | TPN |
| SPN | Y | VARCHAR2(13) | Supplier product ID (VPN) |
| STATNO | Y | VARCHAR2(30) | Article statistical code (Intrastat) |
| CUSTOMS | NaN | VARCHAR2(30) | Article customs code |
| DESCRIPTION | NaN | VARCHAR2(35) | Article description |
| QTYORDER | NaN | NUBMER(11,3) | Quantity in units as on purchase order |
| QTYRECVD | NaN | NUMBER(11,3) | Quantity in units as on VRN |
| CATPRICE | NaN | NUMBER(11,3) | Unit price before discount |
| NETPRICE | NaN | NUMBER(11,3) | Net unit price |
| VATRATE | NaN | NUMBER(6,3) | Actual rate in % |
| UNIT | NaN | VARCHAR2(3) | SKU unit name (UOM) |
| VATCODE | NaN | VARCHAR2(1) | VAT code (S, E)? |

## Change History
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 |
| --- | --- | --- | --- |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| Date | Revision | By | Notes |
| 2007-01-30 00:00:00 | V1.0.0 | Supriyo Chakraborty | NaN |

## Notes
|
|  |