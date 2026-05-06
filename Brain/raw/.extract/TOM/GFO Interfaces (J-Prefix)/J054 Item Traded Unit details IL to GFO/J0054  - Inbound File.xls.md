## Sheet1
| File - JLL.IL.JLTRD.TRADUNIT | File length 82 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Field Name | Referenced in CR? | Insync format | Start | Length | COBOL \nFormat | Description | Mappings |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Header Record | (needs to exist) | G | 1 | 82 | NaN | NaN | NaN |
| JLTRA-REC-TYPE | Y | C 8 | 1 | 1 | X | Record type (‘0’ for Header) | NaN |
| JLTRA-RUN-DATE | Y | C 10 | 2 | 8 | X(8) | Date (CCYYMMDD) of sent file | System Date |
| JLTRA-RUN-TIME | Y | C 6 | 10 | 6 | X(6) | Time (hhmmss) of sent file | System Time |
| JLTRA-BUSINESS-DATE | Y | C 8 | 16 | 8 | X(8) | Business date (CCYYMMDD) - relates to the load date of the Datamart.\n\nSet to SPACES. | Set to spaces |
| FILLER | N | C 59 | 24 | 59 | X(59) | SPACES | Set to spaces |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Detail Record | (needs to exist) | G | 1 | 82 | NaN | NaN | NaN |
| JLTRB-REC-TYPE | Y | C 1 | 1 | 1 | X | Record type (‘1’ for Detail) | NaN |
| JLTRB-TRADTPN | Y | Z 9 | 2 | 9 | 9(9) | Traded unit number | Pack Item Level 1->> Item |
| JLTRB-BASE-PRODUCT-NO | Y | Z 9 | 11 | 9 | 9(9) | Base product number | SKU Item Level 2->> Item |
| JLTRB-TRAD-UNIT-DESC | Y | C 30 | 20 | 30 | X(30) | Traded unit description | Pack Item Level 1->> ItemDesc |
| JLTRB-EEAN | Y | Z 14 | 50 | 14 | 9(14) | Outer case code | Pack Item Level 2->> Item |
| JLTRB-TU-NOTIONAL-WT | Y | Z 5,2 | 64 | 7 | 9(5)V99 | Notional weight of the traded unit.\n\nFor Turkey this weight is in KG.  For USA this weight is in LB (and decimal places of a LB - not ounces).\n\nNot resolved yet so for time being set to ZEROES (i.e. 99999).  Will need to be investigated further. | Set to spaces |
| JLTRB-NOM-PACK-WEIGHT | Y | Z 3,2 | 71 | 5 | 999V99 | Nominal pack weight\n\nFor Turkey this weight is in KG.  For USA this weight is in LB (and decimal places of a LB - not ounces).\n\nNot resolved yet so for time being set to ZEROES (i.e. 99999).  Will need to be investigated further. | Set to spaces |
| JLTRB-UNIT-SIZE-X (group) | Y | G | 76 | 7 | X(7) | Unit size of the traded unit - set to spaces if no unit size exists. | Pack Item BreakOut->>Pack\_Item\_Qty |
| JLTRB-UNIT-SIZE (redef) | Y | Z 5,2 | 76 | 7 | 9(5)V99 | Unit size of the traded unit | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Trailer Record | (needs to exist) | G | 1 | 82 | NaN | NaN | NaN |
| JLTRC-REC-TYPE | Y | C 1 | 1 | 1 | X | Record type (‘9’ for Trailer) | NaN |
| JLTRC-REC-COUNT | Y | Z 9 | 2 | 9 | 9(9) | Record count including the header and trailer records. | Set to spaces |
| FILLER | N | Z 72 | 11 | 72 | X(72) | SPACES | NaN |

## Sheet2
|
|  |

## Sheet3
|
|  |