## Review comments
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Programme name | TOM | Interface Number | TIMS Integration | NaN | NaN | NaN | NaN | NaN | NaN |
| Document title | S035\_InterfaceSpec\_Issues | Document date and/or version | 16/02/2007 | 1.1 | NaN | NaN | NaN | NaN | NaN |
| Location | Description | Severity | Type | Status | Opened by | Open Date (dd/mmm/yyyy) | Closed By | Close Date (dd/mmm/yyyy) | Comments |
| Spec Doc | how to insert data in to the target database? Are we using any commonform in between SSIS and the target db i.e IKB | High | Unclear | Closed | A.Lavanya | 16/02/2007 | NaN | NaN | [NS190207]:We are using Common Forms for this Interface. Since Common forms are being finalized at Offshore, please confirm from Nikhil and Arnab, whether Store Common Form is ready for use. |
| Spec Doc(Target Schema) 4.5 | CustomerProfile,Floors,OpeningDate fields datatype and length not mentioned in spec doc and in mapping doc | Medium | NaN | New | NaN | NaN | NaN | NaN | [NS190207]:Business Clarifications needed on Customer Profile, Floors. Opening Date is not in Common Form which I was referring for stores. Please confirm from Nikhil / James at Offshore if they are available. |
| 4.5 | target Message Schema is not matching with target fields in Mapping doc. | High | Missing | In progress | A.Lavanya | 16/02/2007 | NaN | NaN | [NS190207]:Please use the schema mentioned in the Mapping Document. The actual table Script is not yet received from JDA. Once received , both documents will be made in sync. |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 4.5 | store\_Name and store\_number are missing as they are present in mapping doc target fields | High | Missing | New | A.Lavanya | 16/02/2007 | NaN | NaN | [NS190207]:StoreID is available, Store Name will be added in the Interface will be uploaded soon. |
| 4.5 | field says floors but in mapping doc target fields is No\_of\_floors | Medium | Unclear | New | A.Lavanya | 16/02/2007 | NaN | NaN | [NS190207]:Use Mapping Document for Field Names. |
| Common Forms | we need one node above the Store Node to loop multiple times in TOM.C012ORMStoIDS.Schema.Store.xsd | High | Critical | New | A.Lavanya | 16/02/2007 | NaN | NaN | [NS190207]:Please discuss this with Arnab / Nikhil. |
| NaN | Is the name of the intermediate table in the IKB is Stock Holding Table? Whats the structure of it? | Medium | Unclear | New | Sumit Jain | 19/02/2007 | NaN | NaN | [NS190207]:I need to confirm from JDA on the naming conventions. Please name it as Store Holding Table for the time being till the script is not available. |
| NaN | How do I make sure that when I am reading the data from the store and address tables, I am not reading duplicate data,  I mean the data which I had already read earlier. | Low | Unclear | Closed | Sumit Jain | 19/02/2007 | NaN | NaN | [NS190207]: I need more clarification on this. Is it with respect to Common Forms or exception handling ? If yes than please confirm with Arnab / Nikhil. \nArnab: This is a full drop. So we need not bother whether the data has already been read earlier |
| section 5.9 | Non-Functional Requirements, it says "On successful delivery of the data to the target system, the audit log should be updated via the Operational Framework pipeline component or adapter (to be determined)". But there is no pipeline component or adapter in SSIS. | Medium | Unclear | In progress | Sumit Jain | 19/02/2007 | NaN | NaN | NaN |
| section 5.9 | Also it says "In the event of a failure of transformation of data should be written to the failed log database, and an alert should be raised". Whats the name of the failed log database and what type of alert should be raised. | Medium | Unclear | In progress | Sumit Jain | 19/02/2007 | NaN | NaN | [NS190207] :This should be a part of exception handling for SSIS. Leave the placeholder in the code. TBD |
| Requirements for the End-to-End Interface | What will be the identified cut-off time for populating or delivering the resulting data to IKB Stock Holding Table | Low | Missing | In progress | Sumit Jain | 19/02/2007 | NaN | NaN | TBD |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Requirements for the End-to-End Interface | The interface-run should be non atomic in nature. Appropriate mechanisms should be in place to raise/alert appropriate parties? | Medium | Unclear | In progress | Sumit Jain | 19/02/2007 | NaN | NaN | [NS190207] :This should be a part of exception handling. Leave the placeholder in the code. TBD |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| section 3.2 | Does the row sets representing SKU Items in the Item Common Form. I think it is store common form.\n\n | Critical | Wrong | New | Lavanya | 13/03/2007 | NaN | NaN | [NS190207] : Corrected |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Issues Summary | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Severity | Total | Status | Total | NaN | NaN | NaN | NaN | NaN | NaN |
| Critical | 1 | New | 6 | NaN | NaN | NaN | NaN | NaN | NaN |
| High | 4 | In progress | 5 | NaN | NaN | NaN | NaN | NaN | NaN |
| Medium | 6 | Closed | 2 | NaN | NaN | NaN | NaN | NaN | NaN |
| Low | 2 | Defect raised | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Enhancement | 0 | Rejected | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 13 | Total | 13 | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Type | Total | Time | Hours | NaN | NaN | NaN | NaN | NaN | NaN |
| Missing | 3 | Preparation | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Wrong | 1 | Conduct | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Unclear | 7 | Completion | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Out of scope | 0 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Comment | 0 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 11 | NaN | 0 | NaN | NaN | NaN | NaN | NaN | NaN |

## Options
| Severity | Type | Status |
| --- | --- | --- |
| Critical | Missing | New |
| High | Wrong | In progress |
| Medium | Unclear | Closed |
| Low | Out of scope | Defect raised |
| Enhancement | Comment | Rejected |