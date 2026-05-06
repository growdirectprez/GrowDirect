## GFO Format
| File - JLL.IL.JLPSG | File length 46 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| \*\*\* GFO Format - Different from UK \*\*\* | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Field Name | Referenced in CR? | Insync format | Start | Length | COBOL \nFormat | Description | Mappings |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Header Record | (needs to exist) | G | 1 | 46 | NaN | NaN | NaN |
| JLPS-REC-TYPE | Y | C 1 | 1 | 1 | X | Record type (‘0’ for Header) | NaN |
| JLPS-RUN-DATE | Y | C 8 | 2 | 8 | X(8) | Date (CCYYMMDD) of sent file | System date |
| JLPS-RUN-TIME | Y | C 6 | 10 | 6 | X(6) | Current time in HHMMSS format | System time |
| JLPS-BUSINESS-DATE | Y | C 8 | 16 | 8 | X(8) | Business date of file in CCYYMMDD format.\n\nSet to SPACES. | NaN |
| FILLER | N | C 23 | 24 | 23 | X(23) | SPACES | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Detail Record | (needs to exist) | G | 1 | 46 | NaN | NaN | NaN |
| JLPS-REC-TYPE | Y | C 1 | 1 | 1 | X | Record type (‘1’ for Detail) | NaN |
| JLPS-RMS-COMM-HIER | Y | G | 2 | 20 | NaN | The RMS commercial hierarchy.  This is the equivalent of the Sub group code.  It is a 20 character string split into 5 fields as follows.  CR will translate this into the appropriate CR 5 character Subgroup code. | NaN |
| JLPS-RMS-DIVISION | Y | Z 4 | 2 | 4 | 9(4) | RMS Division for this product.  Equivalent to the UK Division.  Supply as a number with leading zeroes. | Division - >>Division\n\n |
| JLPS-RMS-GROUP | Y | Z 4 | 6 | 4 | 9(4) | RMS Group for this product.  Equivalent to the UK Department.  Supply as a number with leading zeroes.  If this field is not relevant given the level then supply as zero. | Department - >>Department |
| JLPS-RMS-DEPT | Y | Z 4 | 10 | 4 | 9(4) | RMS Department for this product.  Equivalent to the UK Section.  Supply as a number with leading zeroes.  If this field is not relevant given the level then supply as zero. | Section - >>Section |
| JLPS-RMS-CLASS | Y | Z 4 | 14 | 4 | 9(4) | RMS Class for this product.  Equivalent to the UK Product Group.  Supply as a number with leading zeroes.  If this field is not relevant given the level then supply as zero. | Class - >>Class |
| JLPS-RMS-SUBCLASS | Y | Z 4 | 18 | 4 | 9(4) | RMS Sub Class for this product.  Equivalent to the UK Sub Group.  Supply as a number with leading zeroes.  If this field is not relevant given the level then supply as zero. | SubClass - >>SubClass |
| JLPS-SG-LEVEL | Y | C 1 | 22 | 1 | X | Sub group level.  Currently set to a number between 1 and 5 inclusive. | NaN |
| JLPS-HIERARCHY-SUBGROUP-DESC | Y | C 24 | 23 | 24 | X(24) | Subgroup description. | SubClass->>SubClassDesc |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Trailer Record | (needs to exist) | G | 1 | 46 | NaN | NaN | NaN |
| JLPS-REC-TYPE | Y | C 1 | 1 | 1 | X | Record type (‘9’ for Trailer) | NaN |
| JLPS-REC-COUNT | Y | Z 7 | 2 | 7 | 9(7) | Record count including the header and trailer records. | NaN |
| FILLER | N | C 38 | 9 | 38 | X(38) | SPACES | NaN |

## Sheet2
|
|  |

## Sheet3
|
|  |