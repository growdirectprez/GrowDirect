## Denver Lookup
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 |
| --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | PBL | PBS | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | 01  JLPMA-DENVER-HEADER. | NaN | NaN | NaN | NaN |
| NaN | NaN | 03  JLPMA-FILE-KEY-PM          PIC  X(18). | NaN | NaN | NaN | NaN |
| NaN | NaN | 88  DENVER-HEADER VALUE LOW-VALUES. | NaN | NaN | NaN | NaN |
| NaN | NaN | 03  FILLER                     PIC  X(2). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03  JLPMA-FIRST-KEY-EXTRACTED. | First Key  - Date Time will be the same as Last Key, but Sequence number will be different | NaN | NaN | NaN |
| NaN | NaN | 05  JLPMA-FIRST-DATE       PIC  9(8). | NaN | NaN | NaN | NaN |
| NaN | NaN | 05  JLPMA-FIRST-TIME       PIC  9(6). | NaN | NaN | NaN | NaN |
| NaN | NaN | 05  JLPMA-FIRST-SEQ-NO     PIC  9(4). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03  FILLER                     PIC  X(2). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03  JLPMA-LAST-KEY-EXTRACTED. | Last Key | NaN | NaN | NaN |
| NaN | NaN | 05  JLPMA-LAST-DATE        PIC  9(8). | NaN | NaN | NaN | NaN |
| NaN | NaN | 05  JLPMA-LAST-TIME        PIC  9(6). | NaN | NaN | NaN | NaN |
| NaN | NaN | 05  JLPMA-LAST-SEQ-NO      PIC  9(4). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03  FILLER                     PIC  X(2). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03  JLPMA-MOVEMENTS-EXTRACTED  PIC  9(7). | ? | NaN | NaN | NaN |
| NaN | NaN | 03  FILLER                     PIC  X(2). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03  JLPMA-COMPLETION-STATUS-PM PIC  X(8). | ? | NaN | NaN | NaN |
| NaN | NaN | 03  FILLER                     PIC  X. | NaN | NaN | NaN | NaN |
| NaN | NaN | 03  JLPMA-DATE-CREATED-PM      PIC  9(8). | Date Time Stamp | NaN | NaN | NaN |
| NaN | NaN | 03  FILLER                     PIC  X. | NaN | NaN | NaN | NaN |
| NaN | NaN | 03  JLPMA-TIME-CREATED-PM      PIC  9(6). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03  FILLER                     PIC  X. | NaN | NaN | NaN | NaN |
| NaN | NaN | 03  JLPMA-SEQUENCE-NO          PIC  9(10). | Batch Numbers | NaN | NaN | NaN |
| NaN | NaN | 03  FILLER                     PIC  X(96). | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | 01  JLPMB-DENVER-DETAIL. | NaN | NaN | NaN | NaN |
| NaN | NaN | 03 JLPMB-FILE-KEY-PM. | NaN | NaN | NaN | NaN |
| NaN | NaN | 05 JLPMB-KEY-DATE-PM      PIC 9(8). | Date stamp of when Item was picked | NaN | Date and Time Created in IL | NaN |
| NaN | NaN | 05 JLPMB-KEY-TIME-PM      PIC 9(6). | Time of above | NaN | NaN | NaN |
| NaN | NaN | 05 JLPMB-KEY-SEQUENCE-NO-PM | Sequence Number | NaN | NaN | NaN |
| NaN | NaN | PIC 9(4). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03 JLPMB-DIST-WAREHOUSE-GROUP. | NaN | NaN | NaN | NaN |
| NaN | NaN | 05 JLPMB-DISTRIBUTION-CENTRE-PM | NaN | NaN | NaN | NaN |
| NaN | NaN | PIC 9(2). | Default to 00 | NaN | NaN | NaN |
| NaN | NaN | 05 JLPMB-WAREHOUSE-PM     PIC 9(2). | Default to 00 | NaN | NaN | NaN |
| NaN | NaN | 03 JLPMB-PRODUCT-ID-PM       PIC 9(9). | TPND - SKU | NaN | NaN | NaN |
| NaN | NaN | 03 JLPMB-TRANSACTION-TYPE-PM PIC 9(4). | PBL or PBS | NaN | Possible Values 3031 (PBL) and PBS(6112) | NaN |
| NaN | NaN | 03 JLPMB-REASON-CODE-PM      PIC X(2). | Blank | SR | NaN | NaN |
| NaN | NaN | 03 JLPMB-QUANTITY-PM         PIC S9(4). | Number of Pack Picked | Number of Pack Picked | Always Negative | NaN |
| NaN | NaN | 03 JLPMB-MOVEMENT-IN-PM      PIC X(1). | U | U | NaN | NaN |
| NaN | NaN | 03 JLPMB-WEIGHT-PM           PIC 9(4)V99. | Weight of Pack | Weight of Pack | NaN | NaN |
| NaN | NaN | 03 JLPMB-SOURCE-DESTINATION-PM | Store Number | NaN | NaN | NaN |
| NaN | NaN | PIC X(8). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03 JLPMB-REFERENCE-PM        PIC X(8). | Invoice Number | Invoice Number | NaN | NaN |
| NaN | NaN | 03 JLPMB-SCHEDULED-DELY-DATE-PM | Delivery Date | Delivery Date | NaN | NaN |
| NaN | NaN | PIC 9(8). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03 JLPMB-TRANSACTION-ID-PM   PIC X(4). | PLMZ | BOMR | NaN | NaN |
| NaN | NaN | 03 JLPMB-BALANCE-ON-HAND-PM  PIC S9(6). | 0 | 0 | NaN | NaN |
| NaN | NaN | 03 JLPMB-FREE-STOCK-IND-PM   PIC X(01). | Blank | Blank | Ascii 0 | NaN |
| NaN | NaN | 03 JLPMB-PRODUCT-STATUS-PM   PIC 9(01). | 0 | 0 | NaN | NaN |
| NaN | NaN | 03 JLPMB-ORDD-TRADTPN-PM | Blank | Blank | NaN | NaN |
| NaN | NaN | PIC 9(07). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03 JLPMB-ORDERED-QUANTITY-PM PIC S9(04). | Original Qty | Original Qty | NaN | From PO Details Always Positive |
| NaN | NaN | 03 JLPMB-REFUSAL-REASON-PM   PIC X(01). | Blank | NaN | NaN | NaN |
| NaN | NaN | 03 JLPMB-VARIABLE-WGT-FORCED-PM | Blank | NaN | NaN | NaN |
| NaN | NaN | PIC X(01). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03 JLPMB-PURCHASE-ORDER      PIC X(8). | Blank | Blank | NaN | NaN |
| NaN | NaN | 03 JLPMB-DENVER-RECEIPT-NO   PIC X(5). | Blank | Blank | NaN | NaN |
| NaN | NaN | 03 JLPMB-RATIO-PACK          PIC X(01). | Blank | Blank | NaN | NaN |
| NaN | NaN | 03 JLPMB-FILL-UP-TOP-UP      PIC X(01). | Blank | Blank | NaN | NaN |
| NaN | NaN | 88  FILL-UP-ORDER    VALUE "F". | Blank | Blank | NaN | NaN |
| NaN | NaN | 88  TOP-UP-ORDER     VALUE "T". | Blank | Blank | NaN | NaN |
| NaN | NaN | 03 JLPMB-ORDER-TYPE-PM       PIC X(01). | Blank | Blank | NaN | NaN |
| NaN | NaN | 88  NORMAL-ORDER-TYPE      VALUE "N". | Blank | Blank | NaN | NaN |
| NaN | NaN | 88  CONTINGENCY-ORDER-TYPE VALUE "C". | Blank | Blank | NaN | NaN |
| NaN | NaN | 03 JLPMB-BILLED-ORDER-NUMBER-PM | Blank | Blank | NaN | NaN |
| NaN | NaN | PIC X(06). | Blank | Blank | NaN | NaN |
| NaN | NaN | 03 JLPMB-BILLED-ORD-SEG-NUMBER-PM | Blank | Blank | NaN | NaN |
| NaN | NaN | PIC X(03). | Blank | Blank | NaN | NaN |
| NaN | NaN | 03 JLPMB-DELIVERY-WAVE-PM    PIC X(01). | 1 | 1 | NaN | NaN |
| NaN | NaN | 03 JLPMB-CODE-DATE-PM        PIC 9(08). | Shelf Life | Shelf Life | NaN | NaN |
| NaN | NaN | 03 JLPMB-FILLER              PIC X(61). | Blank | NaN | NaN | NaN |
| NaN | NaN | 03 JLPMB-STOCK-CENTRE-NO     PIC 9(5). | DC Number | DC Number | NaN | NaN |
| NaN | NaN | 03 FILLER                    PIC X(3). | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | 01  JLDNV-DENVER-BATCH-REC. | NaN | NaN | NaN | NaN |
| NaN | NaN | 03 JLDNV-KEY                 PIC X(18). | Date Time plus Sequence | NaN | NaN | NaN |
| NaN | NaN | 03 FILLER                    PIC XX. | NaN | NaN | NaN | NaN |
| NaN | NaN | 03 JLDNV-START-DATE          PIC X(8). | Start Date Time | NaN | NaN | NaN |
| NaN | NaN | 03 JLDNV-START-TIME          PIC X(6). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03 FILLER                    PIC X(6). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03 JLDNV-END-DATE            PIC X(8). | End of File Creatation | NaN | NaN | NaN |
| NaN | NaN | 03 JLDNV-END-TIME            PIC X(6). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03 FILLER                    PIC X(4). | NaN | NaN | NaN | NaN |
| NaN | NaN | 03 JLDNV-SEQ-NO              PIC XX. | Batch Number | NaN | NaN | NaN |
| NaN | NaN | 03 JLDNV-REC-COUNT           PIC X(7). | Number of Lines | NaN | NaN | NaN |
| NaN | NaN | 03 JLDNV-DL-SYSTEM-MNEMONIC  PIC XX. | 1 | NaN | NaN | NaN |
| NaN | NaN | 03 FILLER                    PIC X(131). | NaN | NaN | NaN | NaN |