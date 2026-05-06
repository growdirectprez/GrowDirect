## Sheet1
| SLL.STKCENTR.SLD25(0) | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| job JLP10DN0, step SORT20 reformats it into JLL.JLSTKCTR.TODAY, then input into step JLB03 | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| mapped by JLSTKCTR for both today's and yesterday's files | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Field Name | Referenced in CR? | Insync format | Start | Length | COBOL \nFormat | Description | Mapping |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Header record | Must exist | G | 1 | 34 | X(34) | NaN | NaN |
| Filler | Y | C | 1 | 5 | X(5) | set to low values | NaN |
| JLSCA-CNTL-RUN-WK-NO      PIC 99. | Y | Z 2 | 6 | 2 | 99 | Tesco week no - validated vs yesterday's file.  Program logic takes into accoun the change back to week 1. | NaN |
| Filler | NaN | C 27 | 8 | 27 | X(27) | set to spaces | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Detail Record | Must exist | G | 1 | 34 | NaN | stock centre detail record - MUST EXIST | NaN |
| JLSCB-STOCK-CENTRE-NO     PIC X(5). | Y | NaN | 1 | 5 | x(5) | used to update SKC table | NaN |
| FILLER                    PIC XX. | NaN | NaN | 6 | 2 | XX | NaN | NaN |
| JLSCB-STKC-NAME           PIC X(24). | Y | NaN | 8 | 24 | X(24) | Stock centre name.  Used to update SKC table | NaN |
| JLSCB-STKC-ABBR-NAME      PIC XXX. | Y | NaN | 32 | 3 | XXX | Abbreviated 3 character name (for example, appears on delivery list screens).  Updated on SKC table.\n\nIs used on Display screens, reports and as part of delivery confirmation/order routing.  Direct suppliers ABBR name are maintained in CR .  Stock centres could be manually loaded in short term so SET TO SPACES.  This may need to be changed at a later date. | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Trailer record | Must exist | G | NaN | NaN | NaN | trailer record - must exist | NaN |
| Filler | Y | C 5 | 1 | 5 | X(5) | set to high values - needs to be investigated if it can be spaces. | NaN |
| Record Count | Y | Z 8 | 6 | 8 | 9(8) | Record count including header and trailer | NaN |
| Filler | NaN | NaN | 6 | 29 | x(29) | Set to spaces | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| To Clarify : | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| There is no record type specied in the specs | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| In the trailer record,Record count and the Filler starts from the same position. | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| In the header record, The week No represent the week with respective to the year and not with respect to Month | NaN | NaN | NaN | NaN | NaN | NaN | NaN |

## Sheet2
|
|  |

## Sheet3
|
|  |