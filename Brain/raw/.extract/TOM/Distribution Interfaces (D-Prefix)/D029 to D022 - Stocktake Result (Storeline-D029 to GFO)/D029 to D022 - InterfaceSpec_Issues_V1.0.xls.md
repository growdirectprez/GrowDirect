## Review comments
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Programme name | TOM | Project name | TIMS Integration | NaN | NaN | NaN | NaN | NaN | NaN |
| Document title | D029 to D022- StockTake Result | Document date and/or version | <dd/mm/yyyy> | <1.0> | NaN | NaN | NaN | NaN | NaN |
| Location | Description | Severity | Type | Status | Opened by | Open Date (dd/mmm/yyyy) | Closed By | Close Date (dd/mmm/yyyy) | Comments |
| Sec 2.1 | Assumptiion: The stored proc JH0S00 gets stream information by passing some values of the source message (mentioned in sections 4.10, 4.11, 4.12) as attributes to it. After obtaining this stream info, Biztalk has to execute the subsequent stored procs (JIP11,JIP12,JIP13) by passing the stream information and some values of the source message to complete the processing. Also, Biztalk has to check the success/failure of the stored procs. If one of the stored procedures fails, the changes done by the executed stored procs have to be reverted back | Low | Unclear | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | Yes-If the said sp generates error then all other sp execution stpped for the ROWSET.The message then suspended and placed in recoverable mode.The dehydrated msg then call the sp again to get stream inf and in case of success execute corresponding sp subsequently. |
| Sec 2.1 | Mechanism to update the database in GFO in Unix platform from Windows (calling the stored procedures in BizTalk) has to be mentioned in detail. We assume that the DB2 adapter mentioned would be for Windows, but not for cross-platform operation. This has to be made clear | High | Missing | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | Yes-The details to call through DB2 adopter has already sent to you Ravindra & Arnab.We had one discussion regarding this,so plz consult Arnab how to do it? |
| Sec 2.2 | Assumption: The interface is named as ASN in the architecture diagram. We understand it to be Inventory Adjustment | Low | Comment | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | Yes-it is wrongly put as ASN.I will update the interface spec in following days. |
| Sec 3.1 | We are unaware that the source file is dropped on to the share in read only mode.\nWe are developing with the assumption that the file will be created in another location and dropped to the share in non read only mode OR that the file will be created in the share with a read lock during creation and after creation the read lock will be released | Low | Missing | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | The file will be created in the share with a read lock during creation and after creation the read lock will be released. |
| Sec 3.1 | The drop share and the file name created is unknown. These values will be kept configurable and will have to be reconfigured in the before moving to test/production based on environment values | Low | Missing | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | Only Shared location need to be configured.For file name it will be using a \*.dat file. |
| Sec 3.2 | No grouping hierarchy provided for the source message. Also If it is 0 to many in case of detail records does the header record will still exist in the file or not?\nIf header will exist even if detail records is not present then what will be the vaues of the element in Header record | Medium | Unclear | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | It is a envelop type msg schema.This means the source file has one headerwith many detail records. |
| Sec 3.2 | The datatype is not properly defined for the TimeOfExtract and the format In which TimeOfExtract will be, is not mentioed.\nThe datatype string doesnot indicate the number of characters for each data | Medium | Wrong | New | Ajay Gangwar | 2007-02-28 00:00:00 | NaN | NaN | NaN |
| Sec 3.2 | The datatype is not properly defined for the dates and the format In which date will be is not mentioed.\nThe datatype string doesnot indicate the number of characters for each data | Medium | Wrong | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | it will in YYYYMMDD format.The target has the format YYYY-MM-DD. |
| Sec 3.5 | "Name" under section "Biztalk procedure" is not clear . Also the naming standard is incorrect as we are not using underscore("\_") in naming convention | Medium | Unclear | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | The undescore contains in naming structure for the name of interface spec ,so you can remove it & place space in between. I will update the interface spec in following days. |
| Sec 4.8 | There is no information about the database and details about the connectivity. | Medium | Missing | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | Source has flat file and for destination please keep it in a configurable state.Please have a talk with Arnab for destination part before devlelopment. |
| Sec 4.8 | Assumption: In the foot-print of the stored procedure (JH0S00), the input attribute (Store No) from Source field name would be taken from the detail records for every item number which means that the stored procedure would be executed for every item | Medium | Unclear | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | Yes |
| Sec 4.9 | Assumption: In the foot-print of the stored procedure (JIP14), the input attribute (Store No, Item Number, Date of Extract, Time of Extract, Reason Code) from Source field name would be taken from details for every item number which means that the stored procedure would be executed for every item | Medium | Unclear | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | Yes |
| Sec 4.8, 4.9 | The location where the log file should be created should be mentioned | Medium | Missing | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | Yes the path not decided till now - So you please put it in configurable state so that while implementing it will be changed as per the requirement. |
| General | No codepage specified for source and destination messages. UTF-8 (65001) will be used | Low | Missing | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | For Turkey we will use codepage MS28599 for US we will use codepage MS28591.You are doing us dev.\n |
| General | Assumption: Source message files are created with Unique identifiers, so that if Biztalk is not able to process some source messages on time, they will not be overwritten\nDestination files  are created with UniqueIds and timestamp in their names so that one message doesnot override another | Low | Unclear | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | Yes for source file.There is no destination file. |
| General | Sample messages for Source and destination were not available. So, development will proceed with dummy test messages created from the schema definitions provided in the spec. This may affect functional accuracy and quality of unit testing on the interface | Medium | Missing | In progress | Ajay Gangwar | 2007-02-22 00:00:00 | NaN | NaN | I will be sending the sample source data.For destination there will not be any sample data it is only updating the GFO table structure. |
| General | There is no requirement to archive messages after processing, if they are sucessful. Only failed messages are archived to failed folder. The interface uses tracking of message bodies on receive port before processing so that they can be recreated in case of failure | Low | Unclear | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | No archieving is required for faillure it is just writing into a log file. |
| General | Assumption: There is no requirement for ordered delivery of messages | Low | Unclear | Closed | Ajay Gangwar | 2007-02-22 00:00:00 | Mr. Debasis | 2007-02-23 00:00:00 | You are talking it w.r.t calling order of sp.If so then after output attribute field value the next execution will start. |
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
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Issues Summary | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Severity | Total | Status | Total | NaN | NaN | NaN | NaN | NaN | NaN |
| Critical | 0 | New | 1 | NaN | NaN | NaN | NaN | NaN | NaN |
| High | 1 | In progress | 1 | NaN | NaN | NaN | NaN | NaN | NaN |
| Medium | 9 | Closed | 16 | NaN | NaN | NaN | NaN | NaN | NaN |
| Low | 8 | Defect raised | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Enhancement | 0 | Rejected | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 18 | Total | 18 | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Type | Total | Time | Hours | NaN | NaN | NaN | NaN | NaN | NaN |
| Missing | 7 | Preparation | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Wrong | 2 | Conduct | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Unclear | 8 | Completion | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Out of scope | 0 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Comment | 1 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 18 | NaN | 0 | NaN | NaN | NaN | NaN | NaN | NaN |

## Options
| Severity | Type | Status |
| --- | --- | --- |
| Critical | Missing | New |
| High | Wrong | In progress |
| Medium | Unclear | Closed |
| Low | Out of scope | Defect raised |
| Enhancement | Comment | Rejected |