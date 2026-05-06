## Store
| File - CHL.BRANCH.DETAILSR.ALL (CHBCHDER) | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Field Name | Referenced in CR? | Insync format | Start | Length | COBOL Format | Description | Mapping | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| CHBCA-INFO-HDR (group) | Needs to exist. | G | 1 | 325 | X(325) | header rec | NaN | NaN |
| CHBCA-INFO-KEY-GRP (group) | NaN | G | 1 | 6 | X(6) | header rec key | NaN | NaN |
| CHBCA-REC-TYPE\n | Y | Z | 1 | 1 | 9 | Record type :\n0 - Header | NaN | NaN |
| Filler | Y | C | 2 | 316 | X(316) | Low values.  For GFO this can be set to spaces if easier. | NaN | NaN |
| CHBCA-MACH-DTE | Y | Z | 318 | 8 | 9(8) | Date file created. Format CCYYMMDD.  This date is validated against previous day's file (if earlier than previous file then program will abend). | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| CHBCB-INFO-DET-REC (redef) (group) | NaN | G | 1 | 325 | X(325) | detail rec | NaN | NaN |
| CHBCB-INFO-KEY-GRP | NaN | G | 1 | 6 | X(6) | detail rec key | NaN | NaN |
| CHBCB-REC-TYPE | Y | Z | 1 | 1 | 9 | record type '1' | NaN | NaN |
| CHBCB-ORGANISATION-UNIT-NO | Y | Z | 2 | 5 | 9(5) | Retail outlet number | Store -> StoreId | NaN |
| CHBCB-INFO-DATA-GRP (group) | NaN | G | 7 | 319 | X(319) | branch details | NaN | NaN |
| CHBCB-PROPERTY-NO | NaN | Z | 7 | 4 | 9(4) | property number from the OU/PY database to which branch number is linked | ?? | NaN |
| CHBCB-ORG-UNIT-NAME | Y | C | 11 | 21 | X(21) | branch name | Store -> STORE\_NAME | NaN |
| CHBCB-LINE1-ADDRESS | NaN | C | 32 | 24 | X(24) | set to spaces | NaN | NaN |
| CHBCB-LINE2-ADDRESS | NaN | C | 56 | 24 | X(24) | set to spaces | NaN | NaN |
| CHBCB-LINE3-ADDRESS | NaN | C | 80 | 24 | X(24) | set to spaces | NaN | NaN |
| CHBCB-LINE4-ADDRESS | NaN | C | 104 | 24 | X(24) | set to spaces | NaN | NaN |
| CHBCB-POST-CODE | NaN | C | 128 | 12 | X(12) | set to spaces | NaN | NaN |
| CHBCB-RETAIL-OUTLET-TYPE | Y | C | 140 | 1 | X | A very old branch classification :\n1 = store\n2 = H&W\n3 = dummy branch\n5 = PFS\n\nCR only uses this field in one place to identify PFS stores.  It can do this by checking the RO-TYPE-CLASS instead.\n\nSet to SPACE | NaN | NaN |
| CHBCB-RO-PHONE-1-NO | NaN | C | 141 | 17 | X(17) | branch phone number | Store -> PHONE\_NUMBER | NaN |
| CHBCB-RO-TV-REG-NO (occurs 2) | NaN | C | 158 | 2 | XX | NaN | Region -> Region | NaN |
| CHBCB-RO-NLSN-REG-NO | NaN | C | 162 | 2 | XX | Nielsen region - Set to spaces | Region -> Region (only for Nielsen) | NaN |
| CHBCB-DATE-OPENED | Y | C | 164 | 8 | X(8) | original branch opening date - see 'STORE' table in RMS.\nFormat of date DDMMCCYY. | Store -> STORE\_OPEN\_DATE | NaN |
| CHBCB-DATE-CLOSED | Y | C | 172 | 8 | X(8) | date branch ceased trading - see 'STORE' table in RMS.\n\nFormat of date DDMMCCYY. | Store -> STORE\_CLOSE\_DATE | NaN |
| CHBCB-REFIT-DATE | Y | C | 180 | 8 | X(8) | date of last refit - see 'STORE' table in RMS.\n\nFormat of date DDMMCCYY. | Store -> STORE\_REMODELLED\_DATE | NaN |
| CHBCB-ASSOCIATED-UNIT-NO(1) | Y | C | 188 | 5 | X(5) | 'Mother' store (ie main branch if this is a PFS) with leading zeros.  For stores that are not a PFS set to 00000. | Store -> ParentStoreID | NaN |
| CHBCB-ASSOCIATED-UNIT-NO(2) | NaN | C | 193 | 5 | X(5) | child' store (i.e. PFS if this is a main branch)- Set to Spaces | NaN | NaN |
| CHBCB-ASSOCIATED-UNIT-NO(3) | NaN | C | 198 | 5 | X(5) | unused- Set to Spaces | NaN | NaN |
| CHBCB-SITE-LOCN-DESC-CDE | NaN | C | 203 | 5 | X(5) | ?- Set to Spaces | NaN | start position as per our calculation |
| CHBCB-OS-GRID-REF-NO-GRP (group) | NaN | G | 205 | 5 | X(5) | Set to Spaces | NaN | 208 |
| CHBCB-OS-GRID-REF-NO | NaN | PS | 205 | 5 | S9(4)V9(4) \ncomp-3 | Set to Spaces | NaN | 208 |
| CHBCB-OU-DAY-OP-SEG-GRP (group) \noccurs 7 | NaN | G | 210 | 56 | X(56) | these branch opening times are generally thought to be less accurate than those held in C.R. - Set to Spaces | NaN | 213 |
| CHBCB-OU-DLY-OPEN-TIME-GRP (group) | NaN | G | 210 | 4 | X(4) | Set to Spaces | NaN | 213 |
| CHBCB-DAILY-OPENING-HRS | NaN | C | 210 | 2 | XX | Set to Spaces | NaN | 213 |
| CHBCB-DAILY-OPENING-MINS | NaN | C | 212 | 2 | XX | Set to Spaces | NaN | 215 |
| CHBCB-OU-DLY-CLOSE-TIME-GRP (group) | NaN | G | 214 | 4 | X(4) | Set to Spaces | NaN | 217 |
| CHBCB-DAILY-CLOSING-HRS | NaN | C | 214 | 2 | XX | Set to Spaces | NaN | 217 |
| CHBCB-DAILY-CLOSING-MINS | NaN | C | 216 | 2 | XX | Set to Spaces | NaN | 219 |
| CHBCB-REGION-GROUP-NO-GRP | NaN | G | 266 | 3 | XXX | Set to Spaces | NaN | 269 |
| CHBCB-REGION-GROUP-NO | Y | Z | 266 | 3 | 999 | Number of the SD region grouping to which the branch belongs. Recently expanded from 2 to 3 digits.  Does an approriate code exist in RMS? \n\nSet to '000' | NaN | 269 |
| CHBCB-REGION-MD-INITS | NaN | C | 269 | 3 | XXX | initials of the SD for the region - Set to Spaces | NaN | 272 |
| CHBCB-REGION-EXEC-INITS | NaN | C | 272 | 3 | XXX | initials of the OD for the region- Set to Spaces | NaN | 275 |
| CHBCB-TRDG-STAT-CODE | NaN | C | 275 | 1 | X | T - trading\nD - development (not yet open)\nR - currently closed for refit\nC - closed - Set to Spaces | NaN | 278 |
| CHBCB-SHELF-EDGE-LABEL-CD | NaN | C | 276 | 1 | X | Set to Spaces | NaN | 279 |
| CHBCB-MANAGERS-TITLE | NaN | C | 277 | 4 | X(4) | e.g. Mr, Mrs etc - Set to Spaces | NaN | 280 |
| CHBCB-MANAGERS-INITIALS | NaN | C | 281 | 3 | XXX | Set to Spaces | NaN | 284 |
| CHBCB-MANAGERS-NAME | NaN | C | 284 | 16 | X(16) | store manager's surname | Store -> STORE\_MANAGER\_NAME | 287 |
| CHBCB-COUNTY-CODE | Y | C | 300 | 2 | XX | Set to '00' | NaN | 303 |
| CHBCB-CAR-PARK-SPACES-QTY | NaN | PS | 302 | 3 | S9(5) \ncomp-3 | Set to Spaces | NaN | 305 |
| CHBCB-CHECKOUTS-QTY | NaN | PS | 305 | 2 | S999 \ncomp-3 | Set to Spaces | NaN | 308 |
| CHBCB-REGION-CODE | NaN | C | 307 | 1 | X | Old, probably obsolete division, NOT to be confused with Region-Group-No, which is more important. | Region -> Region | 310 |
| CHBCB-COUNTRY-CODE | Y | C | 308 | 1 | X | Current settings\n1 - England\n2 - Wales\n3- Scotland\n4 - France\n5 - Northern Ireland\n7 - ROI\n\nSet to '0' | Coutry Code is not directly related to Location Hierachy | 311 |
| CHBCB-RO-RNGE-CLASS | NaN | C | 309 | 1 | X | branch-level range character which is of limited use since ranging tends to be at MGRP/product level- Set to Spaces | NaN | 312 |
| CHBCB-CPLUS-STORE-IND | NaN | C | 310 | 1 | X | Y or N - Set to Spaces | NaN | 313 |
| CHBCB-METRO-STORE-IND | Y | C | 311 | 1 | X | Current value in UK is Y or N.\n\nIf RO\_TYPE-CLASS='CM' (i.e Metro) Set to 'Y' otherwise set to 'N'. | If (Store -> SellingSqFt) >= 5000 and Store -> SellingSqFt <= 18000 then\n   'Y'\nElse \n   'N' | 314 |
| CHBCB-RO-TYPE-CLASS | Y | C | 312 | 2 | XX | Convert to the CH style codes (see sheet 2 for details).  Code for Hypermarket and supermarket not known yet.  The store type is related to its size in SQR Metre size. | If ((Store -> SellingSqFt) / 10.76) < 300 then\n   'E'\nElsif ((Store -> SellingSqFt) / 10.76) > 300 and ((Store -> SellingSqFt) / 10.76) <= 2000 then\n   'SM'\nElsif ((Store -> SellingSqFt) / 10.76) >= 2500 and ((Store -> SellingSqFt) / 10.76) <= 4500 then\n   'S'\nElsif ((Store -> SellingSqFt) / 10.76) > 5000 then\n   'HY' | 315 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| CHBCZ-INFO-TRLR (redef) (group) | Needs to exist | G | 1 | 325 | X(325) | NaN | NaN | NaN |
| CHBCZ-INFO-KEY-GRP (group) | NaN | G | 1 | 6 | X(6) | NaN | NaN | NaN |
| CHBCZ-REC-TYPE | Y | Z | 1 | 1 | 9 | 9 for trailer | NaN | NaN |
| Filler | Y | C | 2 | 5 | X(5) | High-values.  CR processing does check for this value in program JL0B05, but this program will be changed to reference the record type instead.  If it is easier then set this field to spaces. | NaN | NaN |
| CHBCZ-RECNT | Y | PS | 7 | 5 | 9(5) | The existing UK file has a record count in a packed format (S9(5) comp-3).  However as this field is not currently referenced it can be supplied as a numeric display field instead. | NaN | NaN |
| Filler | N | C | 12 | 314 | X(314) | high-values.  This field is not used so could be set to spaces instead. | NaN | NaN |

## Reference data
| Store types recognised by CH and CR: | Unnamed: 1 | Unnamed: 2 |
| --- | --- | --- |
| NaN | NaN | NaN |
| Existing CH Store type code | Type Description | Tom Store types |
| CM | CLASSIC METRO | Metro - 5-18K SQ, FT |
| D | DOT COM ONLY STORE | NaN |
| E | EXPRESS | Express - Up to 0.3K SQ, MTR, |
| EE | ESSO EXPRESS | NaN |
| ES | EXPRESS STANDALONE | NaN |
| H | HOMEPLUS | NaN |
| HS | HIGH STREET | NaN |
| MB | METRO BADGED | NaN |
| MR | METRO RANGED | NaN |
| P | PETROL FILLING STATION | Petrol Filling Station - Not sure how this is identified? |
| PS | Pet Store (ROI) - no longer used | NaN |
| S | SUPERSTORE | Superstore - 2.5-4.5K SQ, MTR |
| T | TOYS (NI) | NaN |
| W | WINE (NI) | NaN |
| X | EXTRA | NaN |
| NaN | NaN | NaN |
| Codes don’t currently exist in the UK for Hypermarket and Supermarket - so use the following: | NaN | NaN |
| NaN | NaN | NaN |
| HY | NaN | Hypermarket - Over 5K SQ, MTR, |
| SM | NaN | Supermarket - Up to 2K SQ, MTR, |

## Sheet3
|
|  |